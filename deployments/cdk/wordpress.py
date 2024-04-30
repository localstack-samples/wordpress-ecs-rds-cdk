import aws_cdk as cdk
import constructs
from aws_cdk import aws_ec2 as ec2
from aws_cdk import aws_ecs as ecs
from aws_cdk import aws_ecs_patterns as ecs_patterns
from aws_cdk import aws_elasticloadbalancingv2 as elbv2
from aws_cdk import aws_rds as rds

# FIXME
db_user = "wordpress"
db_password = "wordpress-password"
db_name = "wordpress"


class WordpressStack(cdk.Stack):
    def __init__(self, scope: constructs.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # VPC
        self.vpc = ec2.Vpc(
            self,
            "VPC",
            nat_gateways=1,
            ipaddress=ec2.IpAddresses.cidr("10.0.0.0/16"),
            subnet_configuration=[
                ec2.SubnetConfiguration(
                    name="public", subnet_type=ec2.SubnetType.PUBLIC, cidr_mask=24
                ),
                ec2.SubnetConfiguration(
                    name="private", subnet_type=ec2.SubnetType.PRIVATE_WITH_EGRESS, cidr_mask=24
                ),
            ],
        )
        self.cluster_sec_group = ec2.SecurityGroup(
            self,
            "cluster-sec-group",
            security_group_name="cluster-sec-group",
            vpc=self.vpc,
            allow_all_outbound=True,
        )

        database = rds.DatabaseInstance(
            self,
            "WordpressDatabase",
            credentials=rds.Credentials.from_password(
                username=db_user, password=cdk.SecretValue.unsafe_plain_text(db_password)
            ),
            database_name=db_name,
            engine=rds.DatabaseInstanceEngine.MARIADB,
            vpc=self.vpc,
        )

        # ECS cluster
        cluster = ecs.Cluster(self, "ServiceCluster", vpc=self.vpc)

        wp_health_check = ecs.HealthCheck(
            command=['CMD-SHELL', 'curl -s -o /dev/null -w "%{http_code}" http://localhost | grep -qE "200|301|302"'],
            start_period=cdk.Duration.minutes(2)
        )

        docker_image = ecs.ContainerImage.from_registry("wordpress")
        web_service = ecs_patterns.ApplicationLoadBalancedFargateService(
            self,
            "Wordpress",
            cluster=cluster,
            target_protocol=elbv2.ApplicationProtocol.HTTP,
            protocol=elbv2.ApplicationProtocol.HTTP,
            health_check=wp_health_check,
            desired_count=1,
            cpu=512,
            memory_limit_mib=2048,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=docker_image,
                container_port=80,
                container_name="webapp",
                enable_logging=True,
                environment={
                    "WORDPRESS_DB_HOST": f"{database.db_instance_endpoint_address}:{database.db_instance_endpoint_port}",
                    "WORDPRESS_DB_USER": db_user,
                    "WORDPRESS_DB_PASSWORD": db_password,
                    "WORDPRESS_DB_NAME": db_name,
                },
            ),
        )

        web_service.target_group.configure_health_check(
            path="/index.php",
            healthy_http_codes="200,301,302",
            interval=cdk.Duration.seconds(120),
            unhealthy_threshold_count=10
        )

        database.connections.allow_default_port_from(web_service.service.connections)

        # TODO: add APIGW and dns + cert

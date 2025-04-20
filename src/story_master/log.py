import logging


def configure_logger() -> logging.Logger:
    # Initialize variables
    app_name = "story_master"
    logging_level = "INFO"

    # Define format
    logging_format = "%(asctime)s.%(msecs)03d: %(name)s: %(filename)-40s: %(levelname)-10s: %(message)s"
    logging.basicConfig(format=logging_format, datefmt="%Y-%m-%d %H:%M:%S")

    # Create a logger
    logger = logging.getLogger(app_name)
    level = logging.getLevelName(logging_level)
    logger.setLevel(level)

    # Define parameters for logstash handler
    # logstash_host = "logstash_host_xxxx"
    # logstash_port = xxx
    # logstash_logging_timeout = 5.0
    # logstash_ssl_certificate = "/Workspace/ssl_certificates/xxx.crt"

    # Define HTTP Transport for Logstash Handler
    # logstash_transport = HttpTransport(
    #   logstash_host,
    #   logstash_port,
    #   ssl_verify=logstash_ssl_certificate,
    #   timeout=logstash_logging_timeout,
    # )
    #
    # Define Logstash Handler
    # logstash_handler = AsynchronousLogstashHandler(
    #   logstash_host,
    #   logstash_port,
    #   transport=logstash_transport,
    #   database_path="",
    #   ssl_verify=True,
    # )

    # Set Logstash formatter
    # logstash_formatter = LogstashFormatter(extra_prefix=None)
    # logstash_handler.setFormatter(logstash_formatter)

    # Add the logstash handler to the logger
    # logger.addHandler(logstash_handler)

    return logger


logger = configure_logger()

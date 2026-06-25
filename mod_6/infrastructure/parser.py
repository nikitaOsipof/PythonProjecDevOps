#!/usr/bin/env python3
"""
Безопасный парсер конфигураций деплоя
"""
import logging
import yaml

logger = logging.getLogger(__name__)


def load_deploy_config(filepath):
    default_config = {
        "environment": "development",
        "replicas": 1,
    }

    try:
        with open(filepath, "r") as f:
            config_data = yaml.safe_load(f)
            if config_data is None:
                return default_config
            return config_data
    except FileNotFoundError:
        logger.error(f"Конфигурация не найдена по пути: {filepath}")
        return default_config
    except yaml.YAMLError as e:
        logger.error(f"Ошибка синтаксиса в файле {filepath}: {e}")
        return default_config
    except Exception as e:
        return default_config

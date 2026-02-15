"""
Módulo de serviços para o pipeline ETL.

Este pacote contém os serviços de ETL (Extract, Transform, Load)
que orquestram as operações entre os diferentes clientes de dados.
"""

from .etl_service import ETLService

__all__ = ['ETLService']

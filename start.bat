@echo off
python download_ajustes_precos_diesel_e_gasolina.py %*
python download_precos_medios_diesel_e_gasolina.py %*
python atualiza_base_ajuste_precos_diesel_gasolina.py %*
pause
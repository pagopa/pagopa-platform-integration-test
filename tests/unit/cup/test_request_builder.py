"""Unit tests for src/integration/utility/cup/request_builder.py.

These tests are pure unit tests: no network, no behave context, no Allure.
Run with: python -m pytest tests/unit/cup/ -v
"""
import pytest
from src.integration.utility.cup import request_builder


class TestBuildHappyPath:
    def test_contiene_organization_fiscal_code(self):
        body = request_builder.build_happy_path(organization_fiscal_code='01234567890')
        assert '<organizationFiscalCode>01234567890</organizationFiscalCode>' in body

    def test_contiene_id_servizio_cup(self):
        body = request_builder.build_happy_path()
        assert '<idServizio>CUP</idServizio>' in body

    def test_non_contiene_istat_code(self):
        body = request_builder.build_happy_path()
        assert '<istatCode>' not in body

    def test_non_contiene_catast_code(self):
        body = request_builder.build_happy_path()
        assert '<catastalCode>' not in body

    def test_contiene_amount(self):
        body = request_builder.build_happy_path(amount='80.00')
        assert '<amount>80.00</amount>' in body


class TestBuildMultiIdentificativo:
    def test_contiene_organization_e_istat(self):
        body = request_builder.build_multi_identificativo(
            organization_fiscal_code='01234567890',
            istat_code='001234',
        )
        assert '<organizationFiscalCode>01234567890</organizationFiscalCode>' in body
        assert '<istatCode>001234</istatCode>' in body

    def test_contiene_istat_e_catast(self):
        body = request_builder.build_multi_identificativo(
            istat_code='058091',
            catast_code='H501',
        )
        assert '<istatCode>058091</istatCode>' in body
        assert '<catastalCode>H501</catastalCode>' in body


class TestBuildCampiObbligatoriMancanti:
    def test_omette_amount_se_none(self):
        body = request_builder.build_campi_obbligatori_mancanti(amount=None)
        assert '<amount>' not in body

    def test_omette_debtor_full_name_se_none(self):
        body = request_builder.build_campi_obbligatori_mancanti(debtor_full_name=None)
        assert '<debtorFullName>' not in body

    def test_omette_debtor_fiscal_code_se_none(self):
        body = request_builder.build_campi_obbligatori_mancanti(debtor_fiscal_code=None)
        assert '<debtorFiscalCode>' not in body


class TestBuildFormatoErrato:
    def test_preserva_debtor_fiscal_code_errato(self):
        body = request_builder.build_formato_campo_errato(debtor_fiscal_code='00488')
        assert '<debtorFiscalCode>00488</debtorFiscalCode>' in body

    def test_preserva_amount_errato(self):
        body = request_builder.build_formato_campo_errato(amount='500.00')
        assert '<amount>500.00</amount>' in body


class TestBuildNonInCache:
    def test_contiene_istat_no_cache(self):
        body = request_builder.build_non_in_cache(istat_code='noCache')
        assert '<istatCode>noCache</istatCode>' in body

    def test_contiene_catast_no_cache(self):
        body = request_builder.build_non_in_cache(catast_code='noCache')
        assert '<catastalCode>noCache</catastalCode>' in body

    def test_contiene_org_fiscal_no_cache(self):
        body = request_builder.build_non_in_cache(organization_fiscal_code='noCache')
        assert '<organizationFiscalCode>noCache</organizationFiscalCode>' in body

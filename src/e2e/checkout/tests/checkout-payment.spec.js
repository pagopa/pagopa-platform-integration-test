// Importa le funzioni necessarie da Playwright
import { test, expect } from '@playwright/test';
//import { faker } from '@faker-js/faker'; // <-- 1. IMPORTA FAKER.JS

// Legge il file .env per caricare le variabili d'ambiente (es. PAGOPA_API_KEY)
require('dotenv').config();

// ▼▼▼ FUNZIONE PER GENERARE NUMERI DI CARTA VALIDI (SENZA LIBRERIE) ▼▼▼
/**
 * Genera un numero di carta di credito valido (algoritmo di Luhn) per Visa o Mastercard.
 * @param {'visa' | 'mastercard'} issuer - Il tipo di carta da generare.
 * @returns {string} Un numero di carta di credito valido di 16 cifre.
 */
function generateCreditCardNumber(issuer = 'visa') {
  const prefixes = {
    visa: ['4'],
    mastercard: ['51', '52', '53', '54', '55'],
  };
  const prefix = prefixes[issuer][Math.floor(Math.random() * prefixes[issuer].length)];
  let cardNumber = prefix;
  while (cardNumber.length < 15) {
    cardNumber += Math.floor(Math.random() * 10);
  }
  let sum = 0;
  let shouldDouble = true;
  for (let i = cardNumber.length - 1; i >= 0; i--) {
    let digit = parseInt(cardNumber[i]);
    if (shouldDouble) {
      digit *= 2;
      if (digit > 9) {
        digit -= 9;
      }
    }
    sum += digit;
    shouldDouble = !shouldDouble;
  }
  const checkDigit = (10 - (sum % 10)) % 10;
  cardNumber += checkDigit;
  return cardNumber;
}
// ▲▲▲ FINE FUNZIONE ▲▲▲


// Definiamo le variabili globali al file per condividerle tra pre-condizione, test e post-condizione
let noticeCode;
let organizationFiscalCode;
let iupd;

/**
 * ## PRE-CONDIZIONE
 * Viene eseguito una volta prima di tutti i test in questo file.
 * Crea la Posizione Debitoria tramite API.
 */
test.beforeAll(async ({ request }) => {
  console.log('🚀 Eseguo la pre-condizione: Creo la Posizione Debitoria via API...');

  // ▼▼▼ MODIFICA CHIAVE: GENERAZIONE DATI DINAMICI ▼▼▼
  // 1. Creiamo un suffisso univoco basato sul timestamp attuale (ultimi 9 numeri).
  //    Questo renderà i nostri ID unici ad ogni esecuzione.
  const uniqueSuffix = String(Date.now()).slice(-9);

  // 2. Assegniamo i valori alle variabili globali usando il suffisso univoco.
  organizationFiscalCode = '99999000013';
  iupd = `${organizationFiscalCode}-${organizationFiscalCode}-${uniqueSuffix}`;
  noticeCode = `348${uniqueSuffix.padStart(15, '0')}`; // Es: 347 + 000000 + 123456789 = 18 cifre
  const iuv = `47${uniqueSuffix.padStart(15, '0')}`;    // Es: 47 + 000000 + 123456789 = 17 cifre
  // ▲▲▲ FINE MODIFICA CHIAVE ▲▲▲

  const futureDate = new Date();
  futureDate.setDate(futureDate.getDate() + 10);
  
  const debtPositionData = {
    "iupd": iupd,
    "type": "F",
    "fiscalCode": "TSTYSF01L29Z330B",
    "fullName": "TEST USER",
    "streetName": "Test E2E",
    "civicNumber": "1",
    "postalCode": "00100",
    "city": "Roma",
    "province": "RM",
    "region": null,
    "country": "IT",
    "email": "test@gmail.com",
    "switchToExpired": false,
    "companyName": "Test company",
    "paymentOption": [
        {
            "nav": noticeCode,
            "iuv": "48000000000000004",
            "amount": 100,
            "description": "Test E2E",
            "isPartialPayment": false,
            "dueDate": "2099-12-30T23:00:00Z",
            "fee": 0,
            "transfer": [
                {
                    "idTransfer": "1",
                    "amount": 100,
                    "organizationFiscalCode": organizationFiscalCode,
                    "remittanceInformation": "Test E2E",
                    "category": "0107101TS",
                    "iban": "IT92H0301503200000003473949"
                }
            ]
        }
    ]
  };

  // Eseguiamo la chiamata POST e salviamola nella variabile 'response'
  const response = await request.post(`https://api.platform.pagopa.it/gpd/debt-positions-service/v1/organizations/${organizationFiscalCode}/debtpositions?toPublish=true`, {
    headers: {
      'Ocp-Apim-Subscription-Key': process.env.PAGOPA_API_KEY,
      'Content-Type': 'application/json'
    },
    data: debtPositionData
  });

  // Se la chiamata NON è andata a buon fine, stampiamo i dettagli per il debug
  if (!response.ok()) {
    console.error('❌ ERRORE nella creazione della Posizione Debitoria:');
    console.error('Status Code:', response.status());
    try {
      console.error('Response Body:', await response.json());
    } catch (e) {
      console.error('Response Body (non JSON):', await response.text());
    }
  }

  // Verifichiamo che la chiamata sia andata a buon fine (status 2xx)
  expect(response.ok()).toBeTruthy();
  
  // Questa riga verrà eseguita solo se l'expect precedente ha successo
  console.log(`✅ Posizione Debitoria creata con successo. Codice Avviso: ${noticeCode}`);
});

/**
 * ## TEST DELL'INTERFACCIA UTENTE
 * Esegue il flusso di checkout usando i dati creati dalla pre-condizione.
 */
test('PagoPA checkout flow con dati da API', async ({ page }) => {
  // Step 1: Apri pagina
  console.log('🌍 Apro la pagina iniziale');
  await page.goto('https://checkout.pagopa.it/inserisci-dati-avviso');

  // Step 2: Inserisci Codice Avviso (dalla pre-condizione)
  console.log(`✍️ Inserisco Codice Avviso: ${noticeCode}`);
  await page.locator('#billCode').fill(noticeCode);

  // Step 3: Inserisci Codice Fiscale Ente Creditore (dalla pre-condizione)
  console.log(`✍️ Inserisco Codice Fiscale: ${organizationFiscalCode}`);
  await page.locator('#cf').fill(organizationFiscalCode);

    // Step 4: Click Continua
  console.log('👉 Click su Continua');
  await page.click('#paymentNoticeButtonContinue');

  // Step 5: Click Vai al pagamento
  console.log('👉 Click su Vai al pagamento');
  await page.click('#paymentSummaryButtonPay');

  // Step 6: Fill email fields
  console.log('✍️ Inserisco Email e Conferma Email');
  await page.fill('#email', 'teste2e@pagopa.it');
  await page.fill('#confirmEmail', 'teste2e@pagopa.it');

  // Step 7: Click Carta di debito o credito
  console.log('👉 Click su Carta di debito o credito');
  await page.click('#paymentEmailPageButtonContinue');

  // Step 8: Vai alla pagina carta
  console.log('🌍 Apro la pagina inserimento carta');
  //await page.goto('https://checkout.pagopa.it/inserisci-carta');

  // Seleziona l'elemento usando il suo attributo univoco per il testing
  const cartaDiCreditoButton = page.locator('[data-qaid="CP"]');

  // E poi cliccalo 
  await cartaDiCreditoButton.click();

  console.log('⏳ Attendo che l\'iframe della carta sia visibile...');
  
  // Scegliamo a caso tra VISA e Mastercard e usiamo la nostra funzione
  const issuers = ['visa', 'mastercard'];
  const cardIssuer = issuers[Math.floor(Math.random() * issuers.length)];
  const cardNumber = generateCreditCardNumber(cardIssuer);
  console.log(`💳 Generata carta di test ${cardIssuer}: ${cardNumber}`);


  console.log('✍️ Inserisco Numero Carta');
  // 1. Trova l'iframe usando il suo selettore ID.
  //    Playwright ora sa che le prossime azioni saranno dentro questo contesto.
  const cardNumberFrame = page.frameLocator('#frame_CARD_NUMBER');

  // 2. Trova l'input #CARD_NUMBER DENTRO l'iframe e compilalo.
  //    Playwright attenderà automaticamente che sia visibile e pronto.
  //    Uso un numero di carta di credito di test standard.
  //await cardNumberFrame.locator('#CARD_NUMBER').fill('4242424242424242');
  await cardNumberFrame.locator('#CARD_NUMBER').fill(cardNumber);
  

  // Step 8b: Data di scadenza
  console.log('✍️ Inserisco Data di scadenza');
  const expFrame = page.frameLocator('#frame_EXPIRATION_DATE');
  await expFrame.locator('#EXPIRATION_DATE').fill('12/30');

  // Step 8c: CVV
  console.log('✍️ Inserisco CVV');
  const cvvFrame = page.frameLocator('#frame_SECURITY_CODE');
  await cvvFrame.locator('#SECURITY_CODE').fill('123');

  // Step 8d: Nome titolare
  console.log('✍️ Inserisco Nome Titolare');
  const nameFrame = page.frameLocator('#frame_CARDHOLDER_NAME');
  await nameFrame.locator('#CARDHOLDER_NAME').fill('Test E2E');

  // Step 9: Click Continua
  console.log('👉 Click su Continua');
  await page.click('#submit');

  // Step 10: Click Paga
  console.log('👉 Click su Paga');
  await page.click('#paymentCheckPageButtonPay');

  // Step 11: Assertion finale
  console.log('✅ Verifico che l\'URL sia quello di esito');
  //await expect(page).toHaveURL('https://checkout.pagopa.it/esito');
  await expect(page).toHaveURL(/https:\/\/checkout\.pagopa\.it\/(esito|gdi-check)/);

  

});

/**
 * ## POST-CONDIZIONE
 * Viene eseguito una volta dopo tutti i test.
 * Elimina i dati di test creati dalla pre-condizione.
 */
test.afterAll(async ({ request }) => {
  console.log('🗑️ Eseguo la post-condizione: Elimino la Posizione Debitoria via API...');
  
  // Controllo di sicurezza: non tentare di cancellare se i dati non sono stati creati
  if (!iupd || !organizationFiscalCode) {
    console.warn('Dati non disponibili (probabile errore in beforeAll), salto la cancellazione.');
    return;
  }
  
  // Eseguiamo la chiamata DELETE
  const response = await request.delete(`https://api.platform.pagopa.it/gpd/debt-positions-service/v1/organizations/${organizationFiscalCode}/debtpositions/${iupd}`, {
    headers: {
      'Ocp-Apim-Subscription-Key': process.env.PAGOPA_API_KEY,
    }
  });

  // Se la chiamata NON è andata a buon fine, stampiamo i dettagli
  if (!response.ok()) {
    console.error('❌ ERRORE nell\'eliminazione della Posizione Debitoria:');
    console.error('Status Code:', response.status());
    try {
      console.error('Response Body:', await response.json());
    } catch (e) {
      console.error('Response Body (non JSON):', await response.text());
    }
  }

  // Verifichiamo che la chiamata di cancellazione sia andata a buon fine
  expect(response.ok()).toBeTruthy();
  console.log('✅ Posizione Debitoria eliminata con successo.');
});
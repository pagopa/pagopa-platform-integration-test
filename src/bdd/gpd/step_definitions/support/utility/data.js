let gpdSessionBundle = {
    isExecuting: false,
    responseToCheck: undefined,
    organizationCode: undefined,
    brokerCode: undefined,
    stationCode: undefined,
    debtPosition: {
        iupd: undefined,
        iuv1: undefined,
        iuv2: undefined,
        iuv3: undefined,
        iuvOK: undefined,
        iuvKO: undefined,
        iuvPrefix: 'IUV',
        iban: 'mockIban',
        validityDate: undefined,
        dueDate: undefined,
        retentionDate: undefined,
        transferId1: undefined,
        transferId2: undefined,
        receiptId: undefined,
        amount: undefined,
        pspId: undefined,
        pspBrokerId: undefined,
        pspChannelId: undefined,
        pspName: undefined,
        pspFiscalCode: undefined,
        fiscalCode: undefined,
        paymentToken: undefined,
        applicationDate: undefined,
        transferDate: undefined
    },
    payer: {
        name: "Marina Verdi",
        fiscalCode: "VRDMRN72A12H501Z",
        streetName: "Via della Conciliazione",
        civicNumber: "1",
        postalCode: "00100",
        city: "Roma",
        province: "RM",
        region: "LAZ",
        country: "IT",
        email: "marina.verdi@mail.com",
        phone: "333-123456789",
        companyName: "SkyLab Inc.",
        officeName: "SkyLab - Sede via Washington"
    },
}

let gpdUpdateBundle = {
    type: "F",
    fiscalCode: "VRDMRN72A12H501Z",
    fullName: "Marina Verdi",
    companyName: "Testing S.p.A."
}

let gpdPayBundle = {
    paymentDate: "2023-03-10T08:23:52.127Z",
    paymentMethod: "string1",
    pspCompany: "string2",
    idReceipt: "string3",
    fee: 0
                   }

module.exports = {
    gpdSessionBundle,
    gpdUpdateBundle,
    gpdPayBundle,
}
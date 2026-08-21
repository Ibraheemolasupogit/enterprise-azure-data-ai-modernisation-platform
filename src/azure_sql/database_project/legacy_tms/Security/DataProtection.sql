ADD SENSITIVITY CLASSIFICATION TO dbo.CustomerAccount.ContactEmail
WITH (
    LABEL = 'Confidential - Customer Contact',
    INFORMATION_TYPE = 'Contact Info',
    RANK = MEDIUM
);
GO

ADD SENSITIVITY CLASSIFICATION TO dbo.CustomerAccount.LegacyCustomerMemo
WITH (
    LABEL = 'Confidential - Legacy Customer Note',
    INFORMATION_TYPE = 'Customer Content',
    RANK = MEDIUM
);

# OAuth why
- Trust
- Decreased user sensitivity to phishing
- Expanded access and risk
- Limited reliability
- Revocation challenges
- Passwords become required
- Difficulty implementing stronger authentication

-------------------------------------------------------------------

## OAuth Terminology

* Authentication:
  - Process of verifying the identity of a user.
  - Knowing that the user is who they claim to be.
* Federated Authentication:
  - Although many applications have their own system of accounts,
  - including usernames and passwords.
* Authorization:
  - Authorization is the process of verifying that a user has the right to perform some action,
  - such as reading a document or accessing an email account.
* Delegated Authorization:
  - Delegated authorization is granting access to another person,
  - or application to perform actions on your behalf.
  - ( as sudo ? )

-------------------------------------------------------------------

## Tokens : like https://en.wikipedia.org/wiki/Security_token

## Your OAuth Requests:
* => Google =>
  - From Google web or api: Getting the key
  - After Got it => will be able to Making API requests <-- From Your Web App
  
  - ### Authorization Flows ( Ways to send requests ):
    + Authorization code:
      - they are redirected back to the web application,
      - with an authorization code as a query parameter in the URL..
    + Implicit grant for browser-based client-side applications:
      - The resource owner grants access to the application,
      - and a new access token is immediately minted and passed back to
      - the application using a #hash fragment in the URL.
      - **( mined , minted )** ?
    + Resource owner password-based grant:
      - This grant type enables a resource owner’s username and password,
      - user can revoke access to the app without changing the password,
      - and the token is scoped to a limited set of data,
      - so this grant type still provides enhanced security,
      - ( over traditional username/password authentication ).
    + Client credentials:
      - The client credentials grant type allows an application to obtain an access token,
      - for resources owned by the client or when authorization has been:
      - “previously arranged with an authorization server.”
    + Device profile
    + SAML bearer assertion profile

-------------------------------------------------------------------

# A Tour of OpenID

* OpenID:
  - is a system that enables you to use a URL as your identification,
  - and login to any OpenID-enabled web site using that URL.
* You don’t need to create user IDs and passwords on individual web sites.
  - The benefit: As a user of the OpenID system you don’t have to remember,
  - the usernames and passwords for individual web sites.

* create an **OpenID URL** for yourself and then login to OpenID enabled web sites.
  - Also called Consumer or Relying Party or RP using this URL as your identity.
* implementations on the http://openid.net web site.

* understand services like PIP ( web site managing ):
  - Personal Identity Provider or PIP for create an ID.
  - PIP is a service that allows you to create an OpenID identity.

-------------------------------------------------------------------

## OpenID Concepts and Terminology

* End User:
  + End User is the real user or a real person who is using the OpenID system,
  + to login to different web sites using his/her credentials stored,
  + at the Identity Provider
* Consumer or Relying Party (RP):
  - Consumer is the actual web site where you login using OpenID.
  - It is called Consumer because it consumes the OpenID credentials.
* Identifier:
  - Identifier is the URL that identifies digital identity of End User.
* Identity Provider or IdP (OP):
  - Identity Provider or IdP is the host where a user’s credentials are stored.
  - The OpenID URI points to the identity provider.
* User Agent:
  - In simple words, User Agent is your browser.
  - A user interacts with the User Agent directly.

-------------------------------------------------------------------

## Communication among OpenID System Components

* Direct and Indirect Communication
  + Direct => POST,HTTP
  + Indirect =>
    - two entities talk to each other via a third ,
    - entity. This third entity is typically the web browser.
* OpenID Modes of Operation
  + Dumb mode and the Smart mode:
    - Dumb => every time a user logs in.
    - Smart => keep.
  + Is possible using Ajax with Dumb and Smart Modes.

* OpenID Identity URL Page:
  + <link rel=“openid.server”     href=“https://pip.verisignlabs.com”              />
  + <link rel="openid.server"     href="http://idp.conformix.com/index.php/serve"  />
  + <link rel="openid.delegate"   href="http://idp.conformix.com/?user=openidbook" />
  + If the Consumer and Server support OpenID specifications version 2,
  + an XRD document can also be used instead of HTML document.

* OpenID Messages
  + OpenID components exchange different messages during..
    the authentication process.
    These messages have very well defined formats and the Consumers,
    and Identity Providers have to adhere to these formats,
    for successful communication to occur.

* References:
  + For more information, you can refer to the following:
    - OpenID web site at http://openid.net
    - Web site for this book at http://www.openidbook.com
    - Conformix Technologies Inc. http://www.conformix.com
    - OpenID presentation at http://openidbook.com/presentations/COLUG-OpenID.pdf
    - OpenID Blog at http://openid.blogspot.com
    - OpenID information at http://www.openidenabled.com
    - OpenID Directory at http://www.openiddirectory.com

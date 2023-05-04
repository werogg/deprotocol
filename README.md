<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->
[![Build][build-shield]][build-url]
[![Quality][code-quality-shield]][code-quality-url]
[![Coverage][code-coverage-shield]][code-coverage-url]
[![Issues][issues-shield]][issues-url]
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]
[![Discord][discord-shield]][discord-url]



<!-- PROJECT LOGO -->
<br />
<div align="center">
  
  <!-- LOGO DISABLE FOR NOW
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>
  -->

  <h3 align="center">DeProtocol</h3>

  <p align="center">
    A Decentralized and Highly Encrypted P2P Chat over Tor
    <br />
    <a href="https://discord.gg/ZsWt5RdS5E"><strong>Join the Discord »</strong></a>
    <br />
    <br />
    <a href="https://github.com/werogg/deprotocol"><del>View Demo</del></a>
    ·
    <a href="https://github.com/werogg/deprotocol/issues">Report Bug</a>
    ·
    <a href="https://github.com/werogg/deprotocol/issues">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

DeProtcol is a decentralized and highly secure peer-to-peer protocol that provides end-to-end encryption and anonymity for its users. It uses Tor as the underlying network layer to ensure that all communications are routed through multiple relays, making it virtually impossible for anyone to trace the communication back to their origin.

DeChat is designed to be highly resilient and resistant to censorship. Since the application is decentralized, there is no central point of control or failure, making it virtually impossible for any entity to shut down the network or censor individual users.

Here's why:
* Decentralized Peer-to-Peer protocol (no server endings)
* Highly secure with end-to-end encryption
* Anonymized communication relayed in Tor Network
* Highly resilient and resistant to censorship
* File sharing (Soon)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

* [![Python][Python]][Python-url]
* [![Tor][Tor]][Tor-url]

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple example steps.

### Prerequisites

Install Python 3.10: You can download and install Python 3.10 from the official Python website (https://www.python.org/downloads/).

1. Verify python installation:
  ```sh
  python --version
  ```

2. Create a virtual environment (recommended):
  ```sh
  python -m venv myenv
  ```

3. Activate your environment:

  Linux/MacOS: ```source myenv/bin/activate```
    
  Windows: ```myenv\Scripts\activate.bat```
  
### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/werogg/deprotocol.git
   ```

2. Install requirements
   ```sh
   pip install -r requirements.txt
   ```
   
### Execute

1. Run the application
   ```sh
   python src/deprotocol/app/__main__.py
   ```
   
### Build

1. Install additional build requirement
   ```sh
   pip install build
   ```

2. Build the wheel root folder
   ```sh
   python -m build . --wheel
   ```
   
### Run unit tests

1. Install additional pytest requirement
   ```sh
   pip install pytest
   ```

2. Run the tests
   ```sh
   pytest
   ```
   
### Run behaviour tests (not ready)

1. Install additional behave requirement
   ```sh
   pip install behave
   ```

2. Run the tests
   ```sh
   not ready
   ```


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- USAGE EXAMPLES -->
## Usage

Basically when the protocol app is ready it will be prompted in the console, you have a help command to guide you.
My recommendations to test the usage is using **address** command to get the onion address, the **connect** command to connect to an address and finally the **msg** command to test the encrypted byte transmission.


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [x] Add P2P Protocol
- [x] Add Relay on Tor Network
- [ ] Add Custom Communication Protocol (in progress)
- [ ] Add 90% testing for continuous integration
- [ ] Add Protocol API for external uses as lib (in progress)
- [ ] Improve encryption algorithms (in progress)

See the [open issues](https://github.com/werogg/deprotocol/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

Please join our [Discord Server](https://discord.gg/ZsWt5RdS5E) if you would like to contribute, it will be great for me to have a community support to chat about it.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License with Aditional Conditions. See `LICENSE` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

Joel Otero - [@werogg1](https://twitter.com/werogg1) - supwer00@gmail.com

Project Link: [https://github.com/werogg/deprotocol](https://github.com/werogg/deprotocol)

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

Resources and credits!

* [Python](https://www.python.org/)
* [Tor Project](https://www.torproject.org/)
* [University of Barcelona](https://web.ub.edu/es/)
<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[build-shield]: https://img.shields.io/github/actions/workflow/status/werogg/deprotocol/ci.yml?branch=development&style=for-the-badge
[build-url]: https://github.com/othneildrew/deprotocol

[code-quality-shield]: https://img.shields.io/codefactor/grade/github/werogg/deprotocol/development?style=for-the-badge
[code-quality-url]: https://github.com/othneildrew/deprotocol
[code-coverage-shield]: https://img.shields.io/codacy/coverage/66bc32c3001a44899139b5789e68fbc6?style=for-the-badge
[code-coverage-url]: https://github.com/othneildrew/deprotocol
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/othneildrew/Best-README-Template/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/werogg/deprotocol/blob/development/LICENSE
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/joel-otero/
[discord-shield]: https://img.shields.io/badge/Discord-7289DA?style=for-the-badge&logo=discord&logoColor=white
[discord-url]: https://discord.gg/ZsWt5RdS5E

[product-screenshot]: images/screenshot.png
[Python]: https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white
[Python-url]: https://www.python.org/
[Tor]: https://img.shields.io/badge/Tor%20Stem-7D4698?style=for-the-badge&logo=Tor-Browser&logoColor=white
[Tor-url]: https://stem.torproject.org

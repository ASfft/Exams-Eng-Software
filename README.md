# Sistema de Exames Online

## Descrição do Projeto

O Sistema de Exames Online é um projeto desenvolvido para permitir que professores criem exames e estudantes realizem exames de forma online, proporcionando uma experiência amigável e eficiente. O sistema é projetado para ser intuitivo e responsivo, adaptando-se a diferentes dispositivos para oferecer uma experiência consistente.

## 🚀 Getting Started

Clone the project repository from Gitlab
  ```sh
  git clone git@github.com:ASfft/Exams-Eng-Software.git
  ```
Check **Usage** section to handle the project.

### 📋 Prerequisites

* Python 3.10
* [Poetry](https://python-poetry.org/docs/)

### 🔧 Installation

After cloning the project and installing all prerequisites.

* Create a virtual environment

* Check if poetry is using your own virtual environment:
  ```bash
    poetry env system
  ```
* In case poetry is not pointing to correct python path, just update the poetry
  ```bash
    poetry env use system 
  ```
* Install poetry dependencies:

  ```bash
    poetry install
  ```

## 📦 Usage

* Initialize database
  ```sh
    ./manage.py initialize
  ```
* Run application
  ```sh
    python run.py
  ```
  or
  ```sh
    flask --app app.wsgi run
  ```

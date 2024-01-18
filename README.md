<div align='center'>

<img src=https://cdn.buymeacoffee.com/uploads/cover_images/2024/01/elyCMdCeBEB8jMsEKzkFjYwii5kkfcZtDhw50Evf.png@1950w_0e.webp  />

<h1>API for membership weblog</h1>
<p>It is an API for blog that uses various themes and libraries This project can help you have a better understanding of design patterns, API writing, load testing, unit testing, background process, etc., and you can help me in further development and optimization.</p>

<h4> <span> · </span> <a href="https://github.com/Mohammad222PR/weblog.v2/blob/master/README.md"> Documentation </a> <span> · </span> <a href="https://github.com/Mohammad222PR/weblog.v2/issues"> Report Bug </a> <span> · </span> <a href="https://github.com/Mohammad222PR/weblog.v2/issues"> Request Feature </a> </h4>



</div>

# :notebook_with_decorative_cover: Table of Contents

- [About the Project](#star2-about-the-project)
- [FAQ](#grey_question-faq)
- [License](#warning-license)
- [Contact](#handshake-contact)
- [Acknowledgements](#gem-acknowledgements)


## :star2: About the Project
### :space_invader: Tech Stack
<details> <summary>Client</summary> <ul>
<li><a href="https://www.djangoproject.com/">Django</a></li>
<li><a href="https://docs.celeryq.dev/en/stable/index.html">celery</a></li>
<li><a href="https://www.python.org/">python</a></li>
</ul> </details>
<details> <summary>Database</summary> <ul>
<li><a href="">sqlite3</a></li>
<li><a href="">redis</a></li>
</ul> </details>
<details> <summary>DevOps</summary> <ul>
<li><a href="">Docker</a></li>
<li><a href="">Nginx</a></li>
<li><a href="">Guincorn</a></li>
<li><a href="">Github Action</a></li>
</ul> </details>

### :dart: Features
- membership
- jwt auth
- secure
- clean code
- desine pattern
- standard code
- background process


### :art: Color Reference
| Color | Hex |
| --------------- | ---------------------------------------------------------------- |
| Primary Color | ![#d3b9b9](https://via.placeholder.com/10/d3b9b9?text=+) #d3b9b9 |
| Secondary Color | ![#393E46](https://via.placeholder.com/10/393E46?text=+) #393E46 |
| Accent Color | ![#00ADB5](https://via.placeholder.com/10/00ADB5?text=+) #00ADB5 |
| Text Color | ![#EEEEEE](https://via.placeholder.com/10/EEEEEE?text=+) #EEEEEE |

### :key: Environment Variables
To run this project, you will need to add the following environment variables to your .env file
`env`



## :toolbox: Getting Started

### :bangbang: Prerequisites

- install docker<a href="https://www.bing.com/ck/a?!&&p=14926b22282458a5JmltdHM9MTcwNDkzMTIwMCZpZ3VpZD0zNWFiOGNkZC0xNTdjLTY0ZWQtMWFhNy05ZTAzMTRhZTY1YzcmaW5zaWQ9NTE2MA&ptn=3&ver=2&hsh=3&fclid=35ab8cdd-157c-64ed-1aa7-9e0314ae65c7&psq=docker+install&u=a1aHR0cHM6Ly9kb2NzLmRvY2tlci5jb20vZW5naW5lL2luc3RhbGwv&ntb=1"> Here</a>
- install python<a href="https://peps.python.org/pep-0664/"> Here</a>


### :gear: Installation

setup docker
```bash
docker-compose up
```
or
```bash
docker-compose up -d
```
or
```bash
docker-compose up --build -d
```


### :test_tube: Running Tests

test app
```bash
docker-compose exec backend sh -c "pytest ."
```
black formatter
```bash
docker-compose exec backend sh -c "black ."
```
for run flake8
```bash
docker-compose exec backend sh -c "flake8 ."
```


## :wave: Contributing

<a href="https://github.com/Mohammad222PR/weblog.v2.git/graphs/contributors"> <img src="https://contrib.rocks/image?repo=Louis3797/awesome-readme-template" /> </a>

Contributions are always welcome!

see `contributing.md` for ways to get started

### :scroll: Code of Conduct

Please read the [Code of Conduct](https://github.com/Mohammad222PR/weblog.v2.git/blob/master/CODE_OF_CONDUCT.md)

## :grey_question: FAQ

- What should we do if we get into trouble?
- create the issues
- Can we add a new option?
- Yes, you just need to send me your changes with pull request, it will be checked after checking


## :warning: License

Distributed under the no License. See LICENSE.txt for more information.

## :handshake: Contact

mohammadhossein eslami - - mohammades13851@gmail.com

Project Link: [https://github.com/Mohammad222PR/weblog.v2.git](https://github.com/Mohammad222PR/weblog.v2.git)

## :gem: Acknowledgements

Use this section to mention useful resources and libraries that you have used in your projects.

- [pytest]()
- [jwt]()
- [Redis]()
- [celery]()
- [locust]()
- [black]()
- [Faker]()
- [django-celery-beat]()
- [flake8]()
- [drf-yasg]()
- [django-filter]()
- [django-cleanup]()
- [djangorestframework]()
- [ckeditor]()

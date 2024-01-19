import nox

@nox.session
def isort(session):
    session.install("isort")
    session.run("python", "-m", "isort", "serialization_app")

@nox.session
def black(session):
    session.install("black")
    session.run("python", "-m", "black", "--line-length", "88", "serialization_app")

@nox.session
def flake8(session):
    session.install("flake8")
    session.run("python", "-m", "flake8", "serialization_app")

@nox.session
def pylint(session):
    session.install("pylint")
    session.run("python", "-m", "pylint", "serialization_app")
# statannotations-py50

This is a fork of [statannotations](https://github.com/trevismd/statannotations) version 0.6. For anyone interested,
they should use that version directly. This repository will not give details on the inner workings or may ignore major
bugs.

## Why?

The reason why statannotations was forked by me was due to an error I faced with
the [py50-streamlit](https://github.com/tlint101/py50-streamlit/tree/main) application.

During testing on my machine, I found that statannotations did not have major issues with Seaborn v0.12.2. This is
preferable because starting with Seaborn ≥0.12 better control with the error bars on the bar plots was introduced. py50
was then modified to handle Seaborn ≥0.12, despite the constraints put on statannotations. However, I found that there
were issues packaging py50 for PyPi. Specifically, the pacakge manager that I
use, [Poetry](https://github.com/python-poetry/poetry), cannot handle version clashes. While this can be ignored and
Seaborn==0.12.2 can be manually installed on a personal machine or if hosting on a separate server, the dependency
clashes are a huge impediment in deploying it on Streamlit Cloud. As a result, I have forked statannotations and removed
the Seaborn constraint to allow it to handle version 0.12.2. **Everything else in this repository should be the same as
Statannotations v0.6.**

This currently fits my needs and my current timeline. Fixing statannotations itself will require more time and more
familiarity with the coding innards, which I currently do not have much time for.

Again, all credit should be given to [statannotations](https://github.com/trevismd/statannotations).
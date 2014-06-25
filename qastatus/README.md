QAStatus
===================

Extend this project  git@github.com:ralekseenkov/launchpad-reporting.git,
allows to analise information about few projects, collecs statistic


Getting Started
===============

```
# git clone git@github.com:nastya-kuz/akuznetsova
# virtualenv env
# source ./env/bin/activate
# ./install_deps.sh
# ./run_app.sh
```

After that, open http://localhost:4444 in your browser.


How it works
============
- Flask is used as a web frontend
- d3 & nvd3 are used for the charts
- Interation with Launchpad is done through launchpadlib
- The code is optimized to retrieve data from launchpad using the minimum amount of queries. Still, it can take up to 5-10 seconds for a query to complete (for a milestone with hundreds of bugs)
- The results retrieved from Launchpad are cached for 5 minutes. See decorator @ttl_cache


Screenshots
===========
![alt tag](https://github.com/nastya-kuz/akuznetsova/blob/master/qastatus/screenshots/qastatus_main_page.png)
![alt tag](https://github.com/nastya-kuz/akuznetsova/master/qastatus/screenshots/qastatus_bugtrend.png)
![alt tag](https://github.com/nastya-kuz/akuznetsova/master/qastatus/screenshots/qastatus_newbugs_page.png)
![alt tag](https://github.com/nastya-kuz/akuznetsova/master/qastatus/screenshots/qastatus_bugtrend.png)


from datetime import date
from dateutil import relativedelta, parser


from launchpadlib.launchpad import Launchpad
from bug import Bug
from project import Project
from ttl_cache import ttl_cache


class LaunchpadData():

    BUG_STATUSES = {"New":        ["New"],
                    "Incomplete": ["Incomplete"],
                    "Open":       ["Triaged", "In Progress", "Confirmed"],
                    "Closed":     ["Fix Committed", "Fix Released", "Won't Fix", "Invalid", "Expired", "Opinion"]}

    BUG_STATUSES_ALL = []
    for k in BUG_STATUSES:
        BUG_STATUSES_ALL.append(BUG_STATUSES[k])

    def __init__(self):
        cachedir = "~/.launchpadlib/cache/"
        self.launchpad = Launchpad.login_anonymously('launchpad-reporting-www', 'production', cachedir)

    def _get_project(self, project_name):
        return self.launchpad.projects[project_name]

    def _get_milestone(self, project_name, milestone_name):
        project = self._get_project(project_name)
        return self.launchpad.load("%s/+milestone/%s" % (project.self_link, milestone_name))

    @ttl_cache(minutes=5)
    def get_project(self, project_name):
        return Project(self._get_project(project_name))

    @ttl_cache(minutes=5)
    def get_bugs(self, project_name, statuses, milestone_name = None, tags = None):
        project = self._get_project(project_name)
        if (milestone_name is None) or (milestone_name == 'None'):
            return [Bug(r) for r in project.searchTasks(status=statuses)]

        milestone = self._get_milestone(project_name, milestone_name)
        if (tags is None) or (tags == 'None'):
            return [Bug(r) for r in project.searchTasks(status=statuses, milestone=milestone)]

        return [Bug(r) for r in project.searchTasks(status=statuses, milestone=milestone, tags=tags)]

    @staticmethod
    def dump_object(object):
        for name in dir(object):
            try:
                value = getattr(object, name)
            except AttributeError:
                value = "n/a"
            try:
                print name + " --- " + str(value)
            except ValueError:
                print name + " --- " + "n/a"

    def total_number_bugs(self, project_name, tag):

        def get_date(parameter):
            return parser.parse(parameter.ctime())

        week_ago = date.today() - relativedelta.relativedelta(weeks=1)
        months_ago = date.today() - relativedelta.relativedelta(months=1)

        project = self._get_project(project_name)
        statistic = {"total": "",
                     "critical": "",
                     "new_for_week": "",
                     "fixed_for_week": "",
                     "new_for_month": "",
                     "fixed_for_month": ""}

        launchpad_bugs = project.searchTasks(importance=["Critical",],
                                             status=["New",
                                                     "Fix Committed",
                                                     "Confirmed",
                                                     "Triaged",
                                                     "In Progress",
                                                     "Incomplete"],
                                             tags=tag)

        statistic["critical"] = str(len(launchpad_bugs))

        launchpad_bugs = project.searchTasks(status=["New",
                                                     "Won't Fix",
                                                     "Confirmed",
                                                     "Triaged",
                                                     "In Progress",
                                                     "Incomplete"])

        statistic['total_unresolved'] = str(len(launchpad_bugs))
        launchpad_bugs = project.searchTasks(status=["New",
                                                     "Fix Committed",
                                                     "Confirmed",
                                                     "Triaged",
                                                     "In Progress",
                                                     "Incomplete"],
                                             tags=tag)

        statistic["total"] = str(len(launchpad_bugs))

        fixed_on_the_last_month = 0
        created_on_the_last_month = 0
        fixed_on_the_last_week = 0
        created_on_the_last_week = 0
        for bug in launchpad_bugs:
            if get_date(months_ago) < get_date(bug.date_created):
                created_on_the_last_month += 1
            if get_date(week_ago) < get_date(bug.date_created):
                created_on_the_last_week += 1
            if bug.date_fix_committed is not None:
                if get_date(months_ago) < get_date(bug.date_fix_committed):
                    fixed_on_the_last_month += 1
                if get_date(week_ago) < get_date(bug.date_fix_committed):
                    fixed_on_the_last_week += 1

        statistic['new_for_week'] = created_on_the_last_week
        statistic['fixed_for_week'] = fixed_on_the_last_week
        statistic['new_for_month'] = created_on_the_last_month
        statistic['fixed_for_month'] = fixed_on_the_last_month
        return statistic
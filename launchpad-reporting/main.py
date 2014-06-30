#import httplib2
import requests, json, flask
from launchpad.release_chart import ReleaseChart
from launchpad.lpdata import LaunchpadData

#httplib2.debuglevel = 1

app = flask.Flask(__name__)
lpdata = LaunchpadData()

@app.route('/project/<project_name>/bug_table_for_status/<bug_type>/<milestone_name>/bug_list')
def bug_list(project_name, bug_type, milestone_name):
    project = lpdata.get_project(project_name)
    tags = None
    if 'tags' in flask.request.args:
        tags = flask.request.args['tags'].split(',')
    bugs = lpdata.get_bugs(project_name, LaunchpadData.BUG_STATUSES[bug_type], milestone_name, tags)
    return flask.render_template("bug_list.html", project=project, bugs=bugs, bug_type=bug_type, milestone_name=milestone_name, selected_bug_table=True)

@app.route('/project/<project_name>/api/release_chart_trends/<milestone_name>/get_data')
def bug_report_trends_data(project_name, milestone_name):
    data = ReleaseChart(lpdata, project_name, milestone_name).get_trends_data()
    return flask.json.dumps(data)

@app.route('/project/<project_name>/api/release_chart_incoming_outgoing/<milestone_name>/get_data')
def bug_report_get_incoming_outgoing_data(project_name, milestone_name):
    data = ReleaseChart(lpdata, project_name, milestone_name).get_incoming_outgoing_data()
    return flask.json.dumps(data)

@app.route('/project/<project_name>/bug_table_for_status/<bug_type>/<milestone_name>')
def bug_table_for_status(project_name, bug_type, milestone_name):
    project = lpdata.get_project(project_name)
    return flask.render_template("bug_table.html", project=project)

@app.route('/project/<project_name>/bug_trends/<milestone_name>')
def bug_trends(project_name, milestone_name):
    project = lpdata.get_project(project_name)
    return flask.render_template("bug_trends.html", project=project, milestone_name=milestone_name, selected_bug_trends=True)

@app.route('/project/<project_name>')
def project_overview(project_name):
    display = False
    project = lpdata.get_project(project_name)
    if project_name in ("mos", "fuel"):
        display = True
    project.display_name = project.display_name.capitalize()
    statistics = lpdata.total_number_bugs(project_name, None)
    return flask.render_template("project.html",
                                 project=project,
                                 total = statistics['total'],
                                 critical = statistics['critical'],
                                 new_for_week = statistics['new_for_week'],
                                 fixed_for_week = statistics['fixed_for_week'],
                                 new_for_month = statistics['new_for_month'],
                                 fixed_for_month = statistics['fixed_for_month'],
                                 total_unresolved = statistics['total_unresolved'],
                                 selected_overview=True,
                                 display_subprojects = display)

@app.route('/project/<global_project_name>/<project_name>')
def mos_project_overview(global_project_name, project_name):
    project = lpdata.get_project(global_project_name)
    tag = ["{0}".format(project_name), ]
    statistics = lpdata.total_number_bugs(global_project_name, tag)
    return flask.render_template("project.html",
                                 project=project,
                                 tag = project_name,
                                 total = statistics['total'],
                                 critical = statistics['critical'],
                                 new_for_week = statistics['new_for_week'],
                                 fixed_for_week = statistics['fixed_for_week'],
                                 new_for_month = statistics['new_for_month'],
                                 fixed_for_month = statistics['fixed_for_month'],
                                 total_unresolved = statistics['total_unresolved'],
                                 selected_overview=True,
                                 display_subprojects = True)

@app.route('/')
def main_page():
    global_statistic = dict.fromkeys(["Fuel", "MOS", "Murano", "Mistral", "Sahara", "Ceilometer"])
    for pr in global_statistic.keys():
        project_statistic = lpdata.total_number_bugs(pr, None)
        global_statistic['{0}'.format(pr)] = project_statistic
    return flask.render_template("main.html", statistic = global_statistic)

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 4444, threaded = True, debug = True)


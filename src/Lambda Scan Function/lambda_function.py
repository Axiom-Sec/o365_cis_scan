import json
import requests
import boto3
import time
import os
from mailer import *
from o365_cis_db import *
TotalPolicyCount = ""
PassPolicyCount = ""
FailPolicyCount = ""
account = ""
table = []
M365="Office 365"

def gen_html(controlResult, client_id, FailPolicyCount, PassPolicyCount, TotalPolicyCount):

    global table
    Critical = str(get_Severity_Count(controlResult,'Critical'))
    High = str(get_Severity_Count(controlResult,'High'))
    Medium = str(get_Severity_Count(controlResult,'Medium'))
    Low = str(get_Severity_Count(controlResult,'Low'))
    FailPolicyCount = str(get_Failed_Policy_Count(controlResult))
    PassPolicyCount = str(int(TotalPolicyCount) - int(FailPolicyCount))
    table.append("""<!DOCTYPE html>
                    <html>
                    <head>
                        <title>sample</title>
                        <style type="text/css">
                                body{
                                    background: #5e5d5d;
                                }
                                .main{
                                    background: rgba(245,245,245,1);
                                    opacity: 1;
                                    position: relative;
                                }
                                .header{
                                    width: 100%;
                                    height: 142px;
                                    background: rgba(255,255,255,1);
                                    opacity: 1;
                                    position: relative;
                                    top: 0px;
                                    left: 0px;
                                    box-shadow: 0px 4px 4px rgba(0, 0, 0, 0.05999999865889549);
                                    overflow: hidden;
                                }
                                .ai-header{
                                    width: 250px;
                                    height: 56px;
                                    /*background: url(../images/v1_4.png);*/
                                    background-repeat: no-repeat;
                                    background-position: center center;
                                    background-size: cover;
                                    opacity: 1;
                                    position: absolute;
                                    top: 43px;
                                    left: 86px;
                                    overflow: hidden;
                                }
                                .axiom-text{
                                    width: 131px;
                                    color: rgba(33,64,154,1);
                                    position: relative;
                                    top: 0px;
                                    left: 0px;
                                    font-family: Open Sans;
                                    font-weight: ExtraBold;
                                    font-size: 41px;
                                    opacity: 1;
                                    text-align: left;
                                }
                                .io-text {
                                    width: 44px;
                                    color: rgba(39,170,225,1);
                                    position: absolute;
                                    top: 0px;
                                    left: 127   px;
                                    font-family: Open Sans;
                                    font-weight: SemiBold;
                                    font-size: 41px;
                                    opacity: 1;
                                    text-align: left;
                                }
                                .ai-desc{
                                    color: rgba(33,64,154,1);
                                    position: absolute;
                                    top: 50px;
                                    right: 100px;
                                    font-family: IBM Plex Sans;
                                    font-weight: Light;
                                    font-size: 42px;
                                    opacity: 1;
                                    text-align: left;
                                }
                                .report-body{
                                    background: rgba(245,245,245,1);
                                    opacity: 1;
                                    /*position: relative;*/
                                }
                                .report-details{
                                    height: 114px;
                                    background: rgba(33,64,154,1);
                                    opacity: 1;
                                    margin: 30px 100px;
                                    left: 0px;
                                    right: 0px;
                                    background-repeat: no-repeat;
                                    background-position: center center;
                                    background-size: cover;
                                    opacity: 1;
                                    overflow: hidden;
                                }
                                .report-head-text{
                                    width: 341px;
                                    color: rgba(255,255,255,1);
                                    position: absolute;
                                    top: 28px;
                                    left: 24px;
                                    font-family: IBM Plex Sans;
                                    font-weight: Regular;
                                    font-size: 24px;
                                    opacity: 1;
                                    text-align: left;
                                }
                                .details{
                                    width: 758px;
                                    height: 75px;
                                    background: url(../images/v1_10.png);
                                    background-repeat: no-repeat;
                                    background-position: center center;
                                    background-size: cover;
                                    opacity: 1;
                                    position: absolute;
                                    top: 17px;
                                    left: 435px;
                                    overflow: hidden;
                                }
                                .report-info-head{
                                    width: 141px;
                                    color: rgba(255,255,255,1);
                                    position: absolute;
                                    top: 22px;
                                    font-family: IBM Plex Sans;
                                    font-weight: SemiBold;
                                    font-size: 18px;
                                    opacity: 0.3499999940395355;
                                    text-align: left;
                                }
                                .rh-sub-section{
                                    position: absolute;
                                }
                                .scan-info{
                                    left: 475px;
                                }
                                .host-info{
                                    left: 775px;
                                }
                                .report-sub-head{
                                    width: 78px;
                                    color: rgba(39,170,225,1);
                                    position: absolute;
                                    top: 52px;
                                    left: 0px;
                                    font-family: IBM Plex Sans;
                                    font-weight: SemiBold;
                                    font-size: 12px;
                                    opacity: 1;
                                    text-align: left;
                                }
                                .report-sub-text{
                                    width: 367px;
                                    color: rgba(255,255,255,1);
                                    position: absolute;
                                    top: 66px;
                                    left: 0px;
                                    font-family: IBM Plex Sans;
                                    font-weight: SemiBold;
                                    font-size: 18px;
                                    opacity: 1;
                                    text-align: left;
                                }
                                .vul-categories{
                                    margin-bottom: 50px;
                                }
                                .label{
                                    width: 139px;
                                    height: 96px;
                                    /*background: rgba(255,255,255,1);*/
                                    position: relative;
                                    opacity: 1;
                                    border: 1px solid rgba(219,219,219,1);
                                    margin: 0px 10px;
                                    align-items: center;
                                    justify-content: center;
                                }
                                .label-top{
                                    width: 100%;
                                    height: 10px;
                                    background: black;
                                    position: absolute;
                                    top: 0px;
                                }
                                .selected-cat{
                                    background: rgba(255,255,255,1);
                                }
                                .selected-cat:after {
                                  content: '';
                                  position: absolute;
                                  left: 1px;
                                  top: 96px;
                                  left: 55px;
                                  border-top: 15px solid white;
                                  border-left: 15px solid transparent;
                                  border-right: 15px solid transparent;
                                }
                                .count{
                                    text-align: center;
                                    color: rgba(0,0,0,1);
                                    font-family: IBM Plex Sans;
                                    font-weight: SemiBold;
                                    font-size: 32px;
                                }
                                .category{
                                    color: rgba(88,88,88,1);
                                    font-family: IBM Plex Sans;
                                    font-weight: Regular;
                                    font-size: 18px;
                                    opacity: 1;
                                    text-align: center;
                                }
                    
                                .label-critical{
                                    background: rgb(243, 36, 0);
                                }
                                .label-high{
                                    background: rgba(135, 211, 124, 1);
                                }
                                .label-medium{
                                    background: rgba(232,193,52,1);
                                }
                                .cat-high{
                                    color: rgba(224,91,67,1) !important;
                                }
                                .cat-critical{
                                    color: rgba(246, 71, 71, 1) !important;
                                }
                                .cat-medium{
                                    color: rgba(232,193,52,1) !important;
                                }
                                .cat-low{
                                    color: rgba(101,175,123,1) !important;
                                }
                                .hi-sub-sec{
                                    position: absolute;
                                }
                                .ip-sec{
                                    left: 196px;
                                }
                                .os-sec{
                                    left: 410px;
                                }
                                .sub-sec {
                                    margin: 0px 100px;
                                }
                                .vul-sec{
                                    top: 192px;
                                }
                                .passed-sec{
                                    top: 300px
                                }
                                .other-sec{
                                    top: 600px;
                                }
                                .row-heading{
                    				width: 187px;
                    			    opacity: 1;
                    			    margin-top: -2px;
                    			    margin-bottom: 15px;
                                }
                                .sec-heading{
                                    width: auto;
                                    color: rgba(0,0,0,1);
                                    font-family: IBM Plex Sans;
                                    font-weight: SemiBold;
                                    font-size: 18px;
                                    opacity: 1;
                                    text-align: left;
                                    margin-top: 40px;
                                    margin-bottom: 15px;
                                }
                                .table-sec{
                                    width: 100%;
                                    background: white;
                                    padding: 30px;
                                }
                                .table-sec-heading{
                                    font-family: IBM Plex Sans;
                                    font-weight: SemiBold;
                                    font-size: 28px;
                                    opacity: 1;
                                    text-align: left;
                                }
                                .passed-text{
                                    color: rgba(81,175,109,1);
                                }
                                .other-text{
                                    color: rgba(70,123,235,1);
                                }
                                .d-flex {
                                    display: flex;
                                }
                                .all-table .table-body{
                                    height: 360px;
                                    overflow: auto;
                                }
                                .table-head{
                                    border-bottom: 1px solid black;
                                    height: 50px;
                                    align-items: center;
                                }
                                .row{
                                    height: auto;
                                    align-items: center;
                                }
                                .label-high1{
                                    background: rgba(224,91,67,1);
                                }
                                .vul-col-ano{
                                    width: 22%;
                                    padding:0px 30px;
                                }
                                .vul-col-sta{
                                    width: 10%;
                                
                                }
                                .vul-col-sev{
                                    width: 10%;
                                    text-align: left;
                                }
                                .vul-col-bp{
                                    width: 8%;
                                    padding-left: 10px;
                                }
                                .vul-col-com{
                                    width: 49%;
                                }
                                .col-bp{
                                    width: 15%;
                                    padding-left: 10px;
                                }
                                .col-val{
                                    width: 15%;
                                    padding: 0px 50px;
                                }
                                .col-com{
                                    width: 36%;
                                }
                                .blue-row{
                                    background: rgba(246,248,255,1);
                                }
                                .table-thd{
                                    color: rgba(0,0,0,1);
                                    font-family: IBM Plex Sans;
                                    font-weight: SemiBold;
                                    font-size: 19px;
                                    opacity: 0.6000000238418579;
                                    text-align: left;
                                }
                                .table-td{
                                    color: rgba(0,0,0,1);
                                    font-family: IBM Plex Sans;
                                    font-weight: SemiBold;
                                    font-size: 16px;
                                    opacity: 1;
                                    text-align: left;
                                }
                                .button4 {
                                    background-color: white;
                                    color: black;
                                    border: 2px solid #e7e7e7;
                                }
                                .Hover:hover {
                                    background-color: lightsteelblue;
                                    color: black;
                                }

                                .hidden {
                                    display: none;
                                }
                        </style>
                        <link href="https://fonts.googleapis.com/css?family=Open+Sans&amp;display=swap" rel="stylesheet">
                        <link href="https://fonts.googleapis.com/css?family=IBM+Plex+Sans&amp;display=swap" rel="stylesheet">
                    </head>
                    <body>
                        <div class="main">
                            <div class="header">
                                <div class="ai-header">
                                    <span class="axiom-text">Axiom</span>
                                    <span class="io-text">IO</span>
                                </div>
                                <span class="ai-desc">O365 Security Postures </span>
                            </div>
                            <div class="report-body">
                                <div class="report-details">
                                        <div class="rh-sub-section">
                                            <span class="report-head-text">O365 CIS Best Practices </span>
                                        </div>
                                        <div class="rh-sub-section scan-info">
                                            <div class="report-info-head">Scan information</div>
                                            <div class="report-sub-head">Date</div>
                                            <div class="report-sub-text">"""+time.strftime("%c %Z")+"""</div>
                                        </div>
                                        <div class="rh-sub-section host-info">
                                            <span class="report-info-head">Client ID</span>
                                            <div class="hi-sub-sec dns-sec">
                                                <span class="report-sub-head">ID</span>
                                                <span class="report-sub-text">"""+client_id+"""</span>
                                            </div>
                                        </div>
                                </div>
                                <div class="sub-sec vul-sec">
                                    <div class="sec-heading">Policy Compliance</div>
                                    <div class="vul-categories d-flex">
                                        <div class="all d-flex label Hover "onclick="filterSelection('all')">
                                            <div>
                                                <div class="count">"""+TotalPolicyCount+"""</div>
                                                <div class="category">All</div>
                                            </div>
                                        </div>
                                        <div class="critical d-flex label Hover "onclick="filterSelection('Failed')">
                                            <div class="label-top label-critical"></div>
                                            <div>
                                                <div class="count cat-critical">"""+FailPolicyCount+"""</div>
                                                <div class="category">Non-Compliant</div>
                                            </div>
                                        </div>
                                        <div class="high d-flex label Hover "onclick="filterSelection('Passed')">
                                            <div class="label-top label-high"></div>
                                            <div>
                                                <div class="count cat-low">"""+PassPolicyCount+"""</div>
                                                <div class="category">Compliant</div>
                                            </div>
                                        </div>
                                    </div>
                                    <div class="sec-heading">
                                        <div class="cat-critical">* Failed Policies Based on Severity</div>
                                    </div>
                                    <div class="vul-categories d-flex">
                                        <div class="high d-flex label Hover "onclick="filterSelection('Critical')">
                                            <div class="label-top label-critical"></div>
                                            <div>
                                                <div class="count cat-critical">"""+Critical+"""</div>
                                                <div class="category">Critical</div>
                                            </div>
                                        </div>
                                        <div class="critical d-flex label Hover "onclick="filterSelection('High')">
                                            <div class="label-top label-high1"></div>
                                            <div>
                                                <div class="count cat-high">"""+High+"""</div>
                                                <div class="category">High</div>
                                            </div>
                                        </div>
                                        <div class="high d-flex label Hover "onclick="filterSelection('Medium')">
                                            <div class="label-top label-medium"></div>
                                            <div>
                                                <div class="count cat-medium">"""+Medium+"""</div>
                                                <div class="category">Medium</div>
                                            </div>
                                        </div>
                                        <div class="high d-flex label Hover "onclick="filterSelection('Low')">
                                            <div class="label-top label-high"></div>
                                            <div>
                                                <div class="count cat-low">"""+Low+"""</div>
                                                <div class="category">Low</div>
                                            </div>
                                        </div>
                                    </div>""")

def printTable(controlResult,heading):
        global table
        table.append("""	<div class="table-sec">
                            <div class="table-sec-heading all-text">""" + heading + """</div>
                            <div class="table all-table">
                                <div class="d-flex table-head">
                                    <div class="vul-col-bp table-thd" style="
                                        width: 80px;
                                    ">Policy Id</div>
                                    <div class="vul-col-ano table-thd" style="
                                                                                height: 20.333;
                                                                                width: 229.562px;
                                                                            ">Description</div>
                                    <div class="vul-col-sta table-thd" style="
                                                                            width: 102.458px;
                                                                        ">Status</div>
                                    <div class="vul-col-sev table-thd" style="
                                        width: 105.688px;
                                    ">Severity</div>
                                    <div class="vul-col-com table-thd">Comments/Recommendations</div>
                                </div>
                                <div class="table-body"> """)
        #for m, _ in enumerate(controlResult):
        for n in range(len(controlResult)):
                if(n%2 == 0):
                    table.append("""    <div class="d-flex row">
                                            <div class="vul-col-bp table-td">"""+controlResult[n]['ControlId']+"""</div>
                                            <div class="vul-col-ano table-td">"""+controlResult[n]['Description']+"""</div>""")
                else:
                    table.append("""    <div class="d-flex row blue-row">
                                            <div class="vul-col-bp table-td">"""+controlResult[n]['ControlId']+"""</div>
                                            <div class="vul-col-ano table-td">"""+controlResult[n]['Description']+"""</div>""")
                if (controlResult[n]['Result'] == "Passed"):
                    table.append("""<div class="vul-col-sta table-td cat-low">Passed</div>""")
                elif(controlResult[n]['Result'] == "Failed"):
                    table.append("""<div class="vul-col-sta table-td cat-critical">Failed</div>""")
                else:
                    table.append("""<div class="vul-col-sta table-td"></div>""")
                if (controlResult[n]['Severity']=='Critical'):
                    table.append(""" <div class="vul-col-sev table-td cat-critical">"""+controlResult[n]['Severity']+"""</div>""")
                elif(controlResult[n]['Severity']=='High'):
                    table.append(""" <div class="vul-col-sev table-td cat-high">"""+controlResult[n]['Severity']+"""</div>""")
                elif(controlResult[n]['Severity']=='Medium'):
                    table.append(""" <div class="vul-col-sev table-td cat-medium">"""+controlResult[n]['Severity']+"""</div>""")
                elif(controlResult[n]['Severity']=='Low'):
                    table.append(""" <div class="vul-col-sev table-td cat-low">"""+controlResult[n]['Severity']+"""</div>""")
                else:
                    table.append(""" <div class="vul-col-sev table-td"></div>""")

                table.append(""" <div class="vul-col-com table-td">"""+controlResult[n]['comments']+"""</div>
                                    </div>
                                    <div class = "row-heading"></div>""")
                
        table.append(""" </div>
                            </div>
                            </div> <div class="sec-heading"></div>""")

def printFooter():
        global table
        table.append("""   </div> </div>               
                            </div>
                            <script>
                            filterSelection("all");
                            function filterSelection(c) {
                                var x, i,sev,sta;
                                x = document.getElementsByClassName("d-flex row");
                                if (c == "all")
                                {
                                    for (i = 0; i < x.length; i++) 
                                    {
                                        w3RemoveClass(x[i], "hidden");
                                    }
                                }
                                else 
                                {
                                    for (i = 0; i < x.length; i++) 
                                    {
                                        sev = x[i].getElementsByClassName("vul-col-sev table-td")[0].innerHTML;
                                        sta = x[i].getElementsByClassName("vul-col-sta table-td")[0].innerHTML;
                                        if(sev.length == 0)
                                        {
                                            continue;
                                        }
                                        w3RemoveClass(x[i], "hidden");
                                        if (c != "Passed" && c != "Failed")
                                         {
                                            if (sev.toUpperCase() != c.toUpperCase())
                                            {
                                                w3AddClass(x[i], "hidden");
                                            }
                                        }
                                        else {
                                            if (sta.toUpperCase() != c.toUpperCase())
                                            {
                                                w3AddClass(x[i], "hidden");
                                            }
                                        }
                                        if (sev.toUpperCase() == c.toUpperCase()) 
                                        {
                                            if (sta != "Failed") 
                                            {
                                                w3AddClass(x[i], "hidden");
                                            }
                                        }
                                    }
                                }
                                return;
                            }
                            // Add Hidden to Particular Class
                            function w3AddClass(element, name) {
                                var i, arr1, arr2;
                                arr1 = element.className.split(" ");
                                arr2 = name.split(" ");
                                for (i = 0; i < arr2.length; i++) {
                                    if (arr1.indexOf(arr2[i]) == -1) { element.className += " " + arr2[i]; }
                    
                                }
                                return;
                            }
                            // Remove Hidden to particular Class
                            function w3RemoveClass(element, name) {
                                var i, arr1, arr2;
                                arr1 = element.className.split(" ");
                                arr2 = name.split(" ");
                                for (i = 0; i < arr2.length; i++) {
                                    while (arr1.indexOf(arr2[i]) > -1) {
                                        arr1.splice(arr1.indexOf(arr2[i]), 1);
                                    }
                                }
                                element.className = arr1.join(" ");
                                return;
                            }
                    
                            // Add active class to the current button (highlight it)
                            var btnContainer = document.getElementById("myBtnContainer");
                            var btns = btnContainer.getElementsByClassName("btn");
                            for (var i = 0; i < btns.length; i++) {
                                btns[i].addEventListener("click", function () {
                                    var current = document.getElementsByClassName("active");
                                    current[0].className = current[0].className.replace(" active", "");
                                    this.className += " active";
                                });
                            }
                                            </script>  
                                            </body>
                                            </html>""")
        #print(table)
        

def get_Failed_Policy_Count(controlResult):
    count = 0
    for m, _ in enumerate(controlResult):
        for n in range(len(controlResult[m])):          
            if controlResult[m][n]['Result'] == "Failed":
                count = count + 1
    return count

def get_Severity_Count(controlResult,severity):
    """Summary
    Args:
        controlResult (TYPE): Description
    Returns:
        TYPE: Description
    """
    Count = 0
    for m, _ in enumerate(controlResult):
        for n in range(len(controlResult[m])):
            if controlResult[m][n]['Severity'] == severity:
                if controlResult[m][n]['Result'] == "Failed":
                    Count += 1
    return Count


def CIS_1_1_1(access_token):
    headers  = {"Authorization": "Bearer "+access_token}
    response = requests.get("https://graph.microsoft.com/v1.0/security/secureScores", headers=headers)
    output_1=json.loads(response.text)
    designated = []
    result = ""
    count = 0
    for displayName in output_1['value']:
        id = displayName['id']
        response = requests.get("https://graph.microsoft.com/v1.0/security/secureScores/"+id, headers=headers)
        output_self=json.loads(response.text)
        result_1 = ""
        implementationStatus = ""
        try:
            for scores in output_self['controlScores']:
                if scores['controlName'] == "AdminMFAV2":
                    count = count + 1
                    result_1 = "Success"
                    if scores['scoreInPercentage'] != "100":
                        result = "Failed"
                        implementationStatus = scores['implementationStatus']
                        break;
                    break;
            if(result_1 == "Success"):
                break;
        except:
            CIS_1_1_1(access_token)
    if count == 0:
        result = "Failed"
    if result == "Success":
        result = "Passed"
        ext = ""
    else:
        result = "Failed"
        ext = "<br> <B>"+ implementationStatus +"</B>"
    Comments = "Multifactor authentication provides additional assurance that the individual attempting to gain access is who they claim to be. With multifactor authentication, an attacker would need to compromise at least two different authentication mechanisms, increasing the difficulty of compromise and thus reducing the risk"
    comments = Comments + ext
    body = {
        "Result" : result,
        "comments" : comments,
        "Severity" :"High",
        "Description" :"Ensure multifactor authentication is enabled for all users in administrative roles",
        "ControlId" :"1.1.1"
         }

    return body
    # return no_mfaadminusers
    
def CIS_1_1_2(access_token):
    headers  = {"Authorization": "Bearer "+access_token}
    response = requests.get("https://graph.microsoft.com/v1.0/security/secureScores", headers=headers)
    output_1=json.loads(response.text)
    designated = []
    result = ""
    count = 0
    for displayName in output_1['value']:
        id = displayName['id']
        response = requests.get("https://graph.microsoft.com/v1.0/security/secureScores/"+id, headers=headers)
        output_self=json.loads(response.text)
        result_1 = ""
        implementationStatus = ""
        try:
            for scores in output_self['controlScores']:
                if scores['controlName'] == "MFARegistrationV2":
                    count = count + 1
                    result_1 = "Success"
                    if scores['scoreInPercentage'] != "100":
                        result = "Failed"
                        implementationStatus = scores['implementationStatus']
                        break;
                    break;
            if(result_1 == "Success"):
                break;
        except:
            CIS_1_1_2(access_token)
    if count == 0:
        result = "Failed"
    if result == "Success":
        result = "Passed"
        ext = ""
    else:
        result = "Failed"
        ext = "<br> <B>"+ implementationStatus +"</B>"
    Comments = "Multifactor authentication provides additional assurance that the individual attempting to gain access is who they claim to be. With multifactor authentication, an attacker would need to compromise at least two different authentication mechanisms, increasing the difficulty of compromise and thus reducing the risk"
    comments = Comments + ext
    body = {
        "Result" : result,
        "comments" : comments,
        "Severity" :"High",
        "Description" :"Ensure multifactor authentication is enabled for all users in all roles",
        "ControlId" :"1.1.2"
         }

    return body
    
def CIS_1_1_3(access_token):
    headers  = {"Authorization": "Bearer "+access_token}
    response = requests.get("https://graph.microsoft.com/v1.0/security/secureScores", headers=headers)
    output_1=json.loads(response.text)
    designated = []
    result = ""
    count = 0
    for displayName in output_1['value']:
        id = displayName['id']
        response = requests.get("https://graph.microsoft.com/v1.0/security/secureScores/"+id, headers=headers)
        output_self=json.loads(response.text)
        result_1 = ""
        implementationStatus = ""
        try:
            for scores in output_self['controlScores']:
                if scores['controlName'] == "OneAdmin":
                    count = count + 1
                    result_1 = "Success"
                    
                    if not (2 <= int(scores['count']) <= 4):
                        result = "Failed"
                        implementationStatus = scores['implementationStatus']
                        break;
                    break;
            if(result_1 == "Success"):
                break;
        except Exception as e:
            print(str(e))
            # CIS_1_1_3(access_token)
    if count == 0:
        result = "Failed"
    if result == "Success":
        result = "Passed"
        ext = ""
    else:
        result = "Failed"
        ext = "<br> <B>"+ implementationStatus +"</B>"
    Comments = "If there is only one global administrator in a tenant, an additional global administrator will need to be identified and configured. If there are more than four global administrators, a review of role requirements for current global administrators will be required to identify which of the users require global administrator access."
    comments = Comments + ext
    body = {
        "Result" : result,
        "comments" : comments,
        "Severity" :"High",
        "Description" :"Ensure that between two and four global admins are designated.",
        "ControlId" :"1.1.3"
         }

    return body

def CIS_1_1_4(access_token):
    headers  = {"Authorization": "Bearer "+access_token}
    response = requests.get("https://graph.microsoft.com/v1.0/security/secureScores", headers=headers)
    output_1=json.loads(response.text)
    designated = []
    result = ""
    implementationStatus = ""
    count = 0
    for displayName in output_1['value']:
        id = displayName['id']
        response = requests.get("https://graph.microsoft.com/v1.0/security/secureScores/"+id, headers=headers)
        output_self=json.loads(response.text)
        result_1 = ""
        for scores in output_self['controlScores']:
            if scores['controlName'] == "SelfServicePasswordReset":
                count = count + 1
                result_1 = "Success"
                if scores['scoreInPercentage'] != "100":
                    result = "Failed"
                    implementationStatus = scores['implementationStatus']
                    break;
                break;
        if(result_1 == "Success"):
            break;
    if count == 0:
        result = "Failed"
    if result == "Success":
        result = "Passed"
        ext = ""
    else:
        result = "Failed"
        ext = "<br> <B>"+ implementationStatus +"</B>"
    Comments = "Enabling self-service password reset allows users to reset their own passwords in Azure AD.Users will no longer need to engage the helpdesk for password resets, and the password reset mechanism will automatically block common, easily guessable passwords."
    comments = Comments + ext
    body = {
        "Result" : result,
        "comments" : Comments,
        "Severity" :"High",
        "Description" :"Ensure self-service password reset is enabled.",
        "ControlId" :"1.1.4"
         }

    return body
        
def CIS_1_1_6(access_token):
    headers  = {"Authorization": "Bearer "+access_token}
    response = requests.get("https://graph.microsoft.com/v1.0/identity/conditionalAccess/policies", headers=headers)
    output_1=json.loads(response.text)
    count = 0
    result = "Success"
    for displayName in output_1['value']:
        name = displayName['displayName']
        if name == "BlockLegacyAuth":
            count = count + 1
            if displayName['state'] != 'enabled':
                result = "Failed"
                break;
            break;
    if count == 0:
        result = "Failed"
    if result == "Success":
        result = "Passed"
        ext = ""
    else:
        result = "Failed"
    Comments = "Legacy authentication protocols do not support MFA. These protocols are often used by attackers. Blocking legacy authentication makes harder for attackers to gain access."
    body = {
        "Result" : result,
        "comments" : Comments,
        "Severity" :"High",
        "Description" :"Enable Conditional Access policies to block legacy authentication.",
        "ControlId" :"1.1.6"
         }

    return body

def CIS_1_1_9(access_token):
    headers  = {"Authorization": "Bearer "+access_token}
    response = requests.get("https://graph.microsoft.com/v1.0/security/secureScores", headers=headers)
    output_1=json.loads(response.text)
    designated = []
    result = ""
    count = 0
    for displayName in output_1['value']:
        id = displayName['id']
        response = requests.get("https://graph.microsoft.com/v1.0/security/secureScores/"+id, headers=headers)
        output_self=json.loads(response.text)
        result_1 = ""
        for scores in output_self['controlScores']:
            if scores['controlName'] == "SigninRiskPolicy":
                count = count + 1
                result_1 = "Success"
                if scores['scoreInPercentage'] != "100":
                    result = "Failed"
                    implementationStatus = scores['implementationStatus']
                    break;
                break;
        if(result_1 == "Success"):
            break;
    if count == 0:
        result = "Failed"
    if result == "Success":
        result = "Passed"
        ext = ""
    else:
        result = "Failed"
        ext = "<br> <B>"+ implementationStatus +"</B>"
    Comments = "Turning on the sign-in risk policy ensures that suspicious sign-ins are challenged for multifactor authentication."
    comments = Comments + ext
    body = {
        "Result" : result,
        "comments" : comments,
        "Severity" :"High",
        "Description" :"Enable Azure AD Identity Protection sign-in risk policies. ",
        "ControlId" :"1.1.9"
         }

    return body   

def CIS_1_1_10(access_token):
    headers  = {"Authorization": "Bearer "+access_token}
    response = requests.get("https://graph.microsoft.com/v1.0/security/secureScores", headers=headers)
    output_1=json.loads(response.text)
    designated = []
    result = ""
    implementationStatus = ""
    count = 0
    for displayName in output_1['value']:
        id = displayName['id']
        response = requests.get("https://graph.microsoft.com/v1.0/security/secureScores/"+id, headers=headers)
        output_self=json.loads(response.text)
        result_1 = ""
        for scores in output_self['controlScores']:
            if scores['controlName'] == "UserRiskPolicy":
                count = count + 1
                result_1 = "Success"
                if scores['scoreInPercentage'] != "100":
                    result = "Failed"
                    implementationStatus = scores['implementationStatus']
                    break;
                break;
        if(result_1 == "Success"):
            break;
    if count == 0:
        result = "Failed"
    if result == "Success":
        result = "Passed"
        ext = ""
    else:
        result = "Failed"
        ext = "<br> <B>"+ implementationStatus +"</B>"
    Comments = "Turning on user risk policy helps to detect the probability that a user account has been compromised."
    comments = Comments + ext
    body = {
        "Result" : result,
        "comments" : comments,
        "Severity" :"High",
        "Description" :"Enable Azure AD Identity Protection user risk policies.",
        "ControlId" :"1.1.10"
         }

    return body   

def CIS_3_1(access_token):
    headers  = {"Authorization": "Bearer "+access_token}
    response = requests.get("https://graph.microsoft.com/v1.0/security/secureScores", headers=headers)
    output_1=json.loads(response.text)
    designated = []
    result = ""
    count = 0
    implementationStatus = ""
    for displayName in output_1['value']:
        id = displayName['id']
        response = requests.get("https://graph.microsoft.com/v1.0/security/secureScores/"+id, headers=headers)
        output_self=json.loads(response.text)
        result_1 = ""
        try:    
            for scores in output_self['controlScores']:
                if scores['controlName'] == "CustomerLockBoxEnabled":
                    count = count + 1
                    result_1 = "Success"
                    if scores['scoreInPercentage'] != "100":
                        result = "Failed"
                        implementationStatus = scores['implementationStatus']
                        break;
                    break;
            if(result_1 == "Success"):
                break;
        except:
            CIS_3_1(access_token)    
    if count == 0:
        result = "Failed"
    if result == "Success":
        result = "Passed"
        ext = ""
    else:
        result = "Failed"
        ext = "<br> <B>"+ implementationStatus +"</B>"
    Comments = "Enabling this feature protects your data against data spillage and exfiltration"
    comments = Comments + ext
    body = {
        "Result" : result,
        "comments" : comments,
        "Severity" :"High",
        "Description" :"Enable Azure AD Identity Protection user risk policies.",
        "ControlId" :"3.1"
         }

    return body   
            
def CIS_3_4(access_token):
    headers  = {"Authorization": "Bearer "+access_token}
    response = requests.get("https://graph.microsoft.com/v1.0/security/secureScores", headers=headers)
    output_1=json.loads(response.text)
    designated = []
    result = ""
    count = 0
    for displayName in output_1['value']:
        id = displayName['id']
        response = requests.get("https://graph.microsoft.com/v1.0/security/secureScores/"+id, headers=headers)
        output_self=json.loads(response.text)
        result_1 = ""
        implementationStatus = ""
        try:
            for scores in output_self['controlScores']:
                if scores['controlName'] == "DLPEnabled":
                    count = count + 1
                    result_1 = "Success"
                    if scores['scoreInPercentage'] != "100":
                        result = "Failed"
                        implementationStatus = scores['implementationStatus']
                        break;
                    break;
            if(result_1 == "Success"):
                break;
        except:
            CIS_3_4(access_token)
    if count == 0:
        result = "Failed"
    if result == "Success":
        result = "Passed"
        ext = ""
    else:
        result = "Failed"
        ext = "<br> <B>"+ implementationStatus +"</B>"
    Comments = "Enabling DLP policies alerts users and administrators that specific types of data should not be exposed, helping to protect the data from accidental exposure."
    comments = Comments + ext
    body = {
        "Result" : result,
        "comments" : comments,
        "Severity" :"High",
        "Description" :"Ensure DLP policies are enabled.",
        "ControlId" :"3.4"
         }

    return body

def CIS_4_12(access_token):
    headers  = {"Authorization": "Bearer "+access_token}
    response = requests.get("https://graph.microsoft.com/v1.0/domains", headers=headers)
    output_1=json.loads(response.text)
    result = "Failed"
    domainid = []
    for displayName in output_1['value']:
        id = displayName['id']
        response = requests.get("https://graph.microsoft.com/v1.0/domains/"+id+"/serviceConfigurationRecords", headers=headers)
        output_self=json.loads(response.text)
        if len(output_self['value']) != 0:
            for record in output_self['value']:
                if record['recordType'] == "Txt":
                    if record["supportedService"] == "Email":
                        if record['text'] == "v=spf1 include:spf.protection.outlook.com -all":
                            result = "Passed"
                        else:
                            result = "Failed"
                            domainid.append(id)
    if result == "Passed":
        ext = ""
    else:
        result = "Failed"
        ext = "<br> <B>"+ str(domainid) +"</B>"
    Comments = "SPF records allow Exchange Online Protection and other mail systems know where messages from your domains are allowed to originate. This information can be used by that system to determine how to treat the message based on if it is being spoofed or is valid."
    comments = Comments + ext
    body = {
        "Result" : result,
        "comments" : comments,
        "Severity" :"High",
        "Description" :"Ensure that SPF records are published for all Exchange Domains.",
        "ControlId" :"4.12"
         }

    return body

def lambda_handler(event, context):
    access_token = event['access_token']
    O365 = []
    O365.append(CIS_1_1_1(access_token))
    O365.append(CIS_1_1_2(access_token))
    O365.append(CIS_1_1_3(access_token))
    O365.append(CIS_1_1_4(access_token))
    O365.append(CIS_1_1_6(access_token))
    O365.append(CIS_1_1_9(access_token))
    O365.append(CIS_1_1_10(access_token))
    O365.append(CIS_3_1(access_token))
    O365.append(CIS_3_4(access_token))
    O365.append(CIS_4_12(access_token))
    # Join results
    control = []
    control.append(O365)
    
    TotalPolicyCount = str(len(control[0]))
    client_id = event['client_id']
    # Create HTML report file if enabled
    gen_html(control, client_id, FailPolicyCount, PassPolicyCount, TotalPolicyCount)
    printTable(O365,M365)
    printFooter()
    htmlReport=table
    print(htmlReport)
    reportName = "O365_CIS_Report_"+client_id+"_CIS.html"

    tmp_file_path = "/tmp/"+reportName

    Html_file= open(tmp_file_path,"w")

    for item in htmlReport:

        Html_file.write(item)

        Html_file.flush()

    Html_file.close()

    try:
        record = get_record(event['requestId'])
        print(record)
        name = record['data'].get('firstName') + ' ' + record['data'].get('lastName')
        print(name)
        emails = [record['data'].get('email')]
        print(emails)
        subject = "O365 Scan Report"
        print(subject)
        body = """The O365 scan report is attached here \n"""
        print(body)
        # Send scan report email
        
        send_notification(name, subject, body, emails,reportName,tmp_file_path)
        
        update_record(event['requestId'])
        print("record updated....")
    except Exception as e:
        print(str(e))
    
    if os.path.exists(tmp_file_path):

        os.remove(tmp_file_path)

        print("Removed the file : ",tmp_file_path)    

    else:

        print("Sorry, file %s does not exist." % tmp_file_path)

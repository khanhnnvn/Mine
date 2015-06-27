/*
Autor: 		Attila Gerendi
Purpose:	Extension preferences registering
*/

//general
	pref("extensions.acunetixwebscanner.intDebuggLevel", 0);
	pref("extensions.acunetixwebscanner.intStatusMachineRetriggerTime", 50);
	pref("extensions.acunetixwebscanner.boolIsRequestPannelVisible", false);

//request parameter combinator
	pref("extensions.acunetixwebscanner.intMaximumCombinationsGeneratedPerInput", 20);
	pref("extensions.acunetixwebscanner.boolEnableTestCombinationReductionOptimisation", false);
	pref("extensions.acunetixwebscanner.boolEnableAllCombination", false);
	

//scanner request
	pref("extensions.acunetixwebscanner.intRequestTimeOut", 15000);
	pref("extensions.acunetixwebscanner.intMaximumResponseAlowed", 1000000);
	pref("extensions.acunetixwebscanner.intMaximumRetry", 3);

//request extractor
	pref("extensions.acunetixwebscanner.intRequestExtractorRuleLocation", 1);
	pref("extensions.acunetixwebscanner.boolRequestExtractorRuleExtractForms", true);
	pref("extensions.acunetixwebscanner.boolRequestExtractorRuleExtractAnchors", true);
	pref("extensions.acunetixwebscanner.boolRequestExtractorRuleExtractImages", true);
	pref("extensions.acunetixwebscanner.boolRequestExtractorRuleExtractScripts", true);
	
	pref("extensions.acunetixwebscanner.boolRequestExtractorRuleExtractCookie", true);
	pref("extensions.acunetixwebscanner.boolRequestExtractorRuleExtractReferer", false);
	pref("extensions.acunetixwebscanner.boolRequestExtractorRuleExtractUserAgent", false);
	
	pref("extensions.acunetixwebscanner.boolExcludeEquivalentRequest", true);

//logging
	pref("extensions.acunetixwebscanner.boolDeleteLogFilesAtStartup", false);
	pref("extensions.acunetixwebscanner.boolDeleteLogFilesAtScanStart", false);
	//http loging
		pref("extensions.acunetixwebscanner.strHTTPLoginFileName", "c:\\HTTPLog.txt");
		pref("extensions.acunetixwebscanner.boolEnableHTTPLoging", true);
		pref("extensions.acunetixwebscanner.boolLimitHTTPLogingToVulnerablerequest", false);
	//functional logging
		pref("extensions.acunetixwebscanner.boolEnableFunctionalLogging", true);
		pref("extensions.acunetixwebscanner.boolIncludeHTTPLogInFunctionalLog", true);
		pref("extensions.acunetixwebscanner.boolHTTPLogInFunctionalLogOnlyHeaders", true);
		pref("extensions.acunetixwebscanner.strFunctionalLoggingFileName", "c:\\functionalLog.txt");
		
		
//tests
	pref("extensions.acunetixwebscanner.intRegisteredTestNumber", 0);

	pref("extensions.acunetixwebscanner.boolTestEnabled1", false);
	pref("extensions.acunetixwebscanner.strTestName1", "");
	pref("extensions.acunetixwebscanner.boolTestDemo1", false);
	
	pref("extensions.acunetixwebscanner.boolTestEnabled2", false);
	pref("extensions.acunetixwebscanner.strTestName2", "");
	pref("extensions.acunetixwebscanner.boolTestDemo2", false);
	
	pref("extensions.acunetixwebscanner.boolTestEnabled3", false);
	pref("extensions.acunetixwebscanner.strTestName3", "");
	pref("extensions.acunetixwebscanner.boolTestDemo3", false);
	
	pref("extensions.acunetixwebscanner.boolTestEnabled4", false);
	pref("extensions.acunetixwebscanner.strTestName4", "");
	pref("extensions.acunetixwebscanner.boolTestDemo4", false);
	
	pref("extensions.acunetixwebscanner.boolTestEnabled5", false);
	pref("extensions.acunetixwebscanner.strTestName5", "");
	pref("extensions.acunetixwebscanner.boolTestDemo5", false);
	
	pref("extensions.acunetixwebscanner.boolTestEnabled6", false);
	pref("extensions.acunetixwebscanner.strTestName6", "");
	pref("extensions.acunetixwebscanner.boolTestDemo6", false);
	
	pref("extensions.acunetixwebscanner.boolTestEnabled7", false);
	pref("extensions.acunetixwebscanner.strTestName7", "");
	pref("extensions.acunetixwebscanner.boolTestDemo7", false);
	
	pref("extensions.acunetixwebscanner.boolTestEnabled8", false);
	pref("extensions.acunetixwebscanner.strTestName8", "");
	pref("extensions.acunetixwebscanner.boolTestDemo8", false);
	
	pref("extensions.acunetixwebscanner.boolTestEnabled9", false);
	pref("extensions.acunetixwebscanner.strTestName9", "");
	pref("extensions.acunetixwebscanner.boolTestDemo9", false);
	
	pref("extensions.acunetixwebscanner.boolTestEnabled10", false);
	pref("extensions.acunetixwebscanner.strTestName10", "");
	pref("extensions.acunetixwebscanner.boolTestDemo10", false);
	
	pref("extensions.acunetixwebscanner.boolTestEnabled11", false);
	pref("extensions.acunetixwebscanner.strTestName11", "");
	pref("extensions.acunetixwebscanner.boolTestDemo11", false);
	
	pref("extensions.acunetixwebscanner.boolTestEnabled12", false);
	pref("extensions.acunetixwebscanner.strTestName12", "");
	pref("extensions.acunetixwebscanner.boolTestDemo12", false);
	
	pref("extensions.acunetixwebscanner.boolTestEnabled13", false);
	pref("extensions.acunetixwebscanner.strTestName13", "");
	pref("extensions.acunetixwebscanner.boolTestDemo13", false);
	
	pref("extensions.acunetixwebscanner.boolTestEnabled14", false);
	pref("extensions.acunetixwebscanner.strTestName14", "");
	pref("extensions.acunetixwebscanner.boolTestDemo14", false);
	
	pref("extensions.acunetixwebscanner.boolTestEnabled15", false);
	pref("extensions.acunetixwebscanner.strTestName15", "");
	pref("extensions.acunetixwebscanner.boolTestDemo15", false);
	
	pref("extensions.acunetixwebscanner.boolTestEnabled16", false);
	pref("extensions.acunetixwebscanner.strTestName16", "");
	pref("extensions.acunetixwebscanner.boolTestDemo16", false);
	
	pref("extensions.acunetixwebscanner.boolOpenResultInFirefox", true);
	pref("extensions.acunetixwebscanner.boolOpenResultInWVS", false);




from burp import IBurpExtender
from burp import IHttpListener
from burp import IProxyListener
from java.io import PrintWriter
import urlparse, json, Cookie, cgi
from StringIO import StringIO as IO
class BurpExtender(IBurpExtender, IHttpListener, IProxyListener):
	def registerExtenderCallbacks(self, callbacks):
		# keep a reference to our callbacks object
		self._callbacks = callbacks
		self._helpers = callbacks.getHelpers()
		self.all_params = dict()
		# obtain our output stream
		self._stdout = PrintWriter(callbacks.getStdout(), True)
		# set our extension name
		callbacks.setExtensionName("Burp Plugin For HTTP Analysis")
		# register ourselves as an HTTP listener
		callbacks.registerHttpListener(self)
		# register ourselves as a Proxy listener
		callbacks.registerProxyListener(self)
		return

	def processHttpMessage(self, toolFlag, messageIsRequest, currentRequest):
		return
	def processProxyMessage(self, messageIsRequest, message):
		if not messageIsRequest:
			# self._stdout.println("Proxy response from " + message.getMessageInfo().getHttpService().toString())
			# self._stdout.println(message.getMessageInfo().getRequest().tostring())
			self.extractParameter(message.getMessageInfo())
			self.checkReflectedXSS(message.getMessageInfo())
		return
	def extensionUnloaded(self):
		self._stdout.println("Extension was unloaded")
		return
	def checkMutiPart(self, headers):
		for i in headers:
			if (i.lower()[:12] == "content-type"):
				if(i.lower()[12:].find("multipart/form-data") > 0 ):
					return True, i
				else:
					return False, None
				break
		return False, None
	def parseMutiPart(self, request_headers, content_type_line):
		body = request_headers.split("\r\n\r\n")[1:]
		body = ("\r\n\r\n".join(body))
		parsed = cgi.FieldStorage(
			IO(body),
			headers={content_type_line},
			environ={'REQUEST_METHOD': 'POST'})
		# Stuck here, wait
	def checkJsonString(self, check_str):
		try:
			json_object = json.loads(check_str)
		except ValueError, e:
			return False # invalid json
		else:
			return True # valid json
	def extractParameter(self, message_info):
		# Extract
		domain = message_info.getHttpService().toString()
		request_headers = message_info.getRequest().tostring()
		request_headers = request_headers.split("\r\n")
		url = request_headers[0].split(" ")[1]
		if (url.find("?") > 0):
			params = urlparse.parse_qsl(url.split("?")[1])
			for x, y in params:
				self.all_params.update({x:y})
		# Check if POST
		if request_headers[0].split(" ")[0] == "POST":
			# Check multipart or not
			check_Multipart, content_type_line = self.checkMutiPart(request_headers)
			if(check_Multipart):
				self.parseMutiPart(message_info.getRequest().tostring(), content_type_line)
			else:
				tmp = request_headers[-1]
				# Check json
				if(self.checkJsonString(tmp)):
					pass # is json
				else:
					# normal case
					params = urlparse.parse_qsl(tmp)
					for x, y in params:
						self.all_params.update({x:y})
		if (len(self.all_params) > 0):
			pass
	def checkReflectedXSS(self, message_info):
		response = message_info.getResponse().tostring()
		domain = message_info.getHttpService().toString()
		request_headers = message_info.getRequest().tostring()
		request_headers = request_headers.split("\r\n")
		url = request_headers[0].split(" ")[1]
		for k in self.all_params.keys():
			value = self.all_params[k]
			# Filter length > 3
			if((len(value)>3) and (response.find(value) > 0)):
				# May be reflected
				self._stdout.println("Refected XSS predict: Found parameter {0}, value {1} in response. URL: {2}{3}".format(k, value, domain, url))

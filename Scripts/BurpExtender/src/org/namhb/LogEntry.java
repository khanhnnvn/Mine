/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package org.namhb;

import burp.IHttpRequestResponsePersisted;
import java.net.URL;

/**
 *
 * @author namhb1
 */
public class LogEntry {
    final int tool;
    final IHttpRequestResponsePersisted requestResponse;
    final URL url;

    LogEntry(int tool, IHttpRequestResponsePersisted requestResponse, URL url)
    {
        this.tool = tool;
        this.requestResponse = requestResponse;
        this.url = url;
    }
}

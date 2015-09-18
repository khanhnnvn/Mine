package burp;

import java.awt.Component;
import java.awt.BorderLayout;
import javax.swing.*;
import javax.swing.BoxLayout;
import net.miginfocom.layout.*;
import net.miginfocom.swing.*;
import java.awt.Button;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Label;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import javax.swing.table.AbstractTableModel;
import javax.swing.table.DefaultTableModel;
import javax.swing.table.TableModel;
public class BurpExtender implements IBurpExtender, ITab, IHttpListener, IMessageEditorController
{
    public IBurpExtenderCallbacks callbacks;
    public IExtensionHelpers helpers;
    public IHttpRequestResponse currentlyDisplayedItem;
    private Gui jPanel1;
    @Override
    public void registerExtenderCallbacks(final IBurpExtenderCallbacks callbacks)
    {
        // your extension code here
        this.callbacks = callbacks;
        callbacks.setExtensionName("NamHB Extension");
        helpers = callbacks.getHelpers();
        SwingUtilities.invokeLater(new Runnable() {
            @Override
            public void run(){
                // table of log entries
                jPanel1 = new Gui(BurpExtender.this);
                callbacks.addSuiteTab(BurpExtender.this);
                callbacks.registerHttpListener(BurpExtender.this);
            }
        });
    }
    @Override
    public void processHttpMessage(int toolFlag, boolean messageIsRequest, IHttpRequestResponse messageInfo)
    {
        // only process responses
        if (!messageIsRequest)
        {
            // create a new log entry with the message details
                jPanel1.addRowDataModel(toolFlag, messageInfo);
        }
    }
    @Override
    public String getTabCaption () {
        return "Extension" ;
    }
    @Override
    public Component getUiComponent () {
        return  jPanel1;
    }
    //
    // implement IMessageEditorController
    // this allows our request/response viewers to obtain details about the messages being displayed
    //
    
    @Override
    public byte[] getRequest()
    {
        return currentlyDisplayedItem.getRequest();
    }

    @Override
    public byte[] getResponse()
    {
        return currentlyDisplayedItem.getResponse();
    }

    @Override
    public IHttpService getHttpService()
    {
        return currentlyDisplayedItem.getHttpService();
    }
}
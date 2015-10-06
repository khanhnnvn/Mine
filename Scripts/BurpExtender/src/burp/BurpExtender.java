package burp;

import org.namhb.Gui;
import java.awt.Component;
import java.util.ArrayList;
import java.util.List;
import javax.swing.*;
import org.namhb.*;

public class BurpExtender implements IBurpExtender, ITab, IHttpListener, IMessageEditorController, IContextMenuFactory 
{
    public IBurpExtenderCallbacks callbacks;
    public IExtensionHelpers helpers;
    public IHttpRequestResponse currentlyDisplayedItem;
    public Gui jPanel1;
    @Override
    public void registerExtenderCallbacks(final IBurpExtenderCallbacks callbacks)
    {
        // your extension code here
        this.callbacks = callbacks;
        helpers = callbacks.getHelpers();

        callbacks.setExtensionName("NamHB Extension");
        callbacks.registerContextMenuFactory(this);
        
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
            //create a new log entry with the message details
            //    jPanel1.addRowDataModel(toolFlag, messageInfo);
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

    @Override
    public List<JMenuItem> createMenuItems(IContextMenuInvocation invocation) {
        //Menu right click
        List <JMenuItem> menuList = new  ArrayList<>(); 
        JMenu sendToItem = new org.namhb.MenuClick(invocation);
        menuList.add(sendToItem);
        return menuList;
        
    }
    
}

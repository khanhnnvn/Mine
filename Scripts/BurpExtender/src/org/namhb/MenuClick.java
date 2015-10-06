/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package org.namhb;

import burp.BurpExtender;
import burp.IBurpExtender;
import burp.IBurpExtenderCallbacks;
import burp.IContextMenuFactory;
import burp.IContextMenuInvocation;
import burp.IExtensionHelpers;
import burp.IHttpRequestResponse;
import burp.IMenuItemHandler;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.List;
import javax.swing.JMenu;
import javax.swing.JMenuItem;

/**
 *
 * @author habachnam
 */
public class MenuClick extends JMenu {
    public JMenuItem sqlClick, xssClick, fileClick;
    public IContextMenuInvocation invocation;
    public IHttpRequestResponse messageinfo;
    public MenuClick(IContextMenuInvocation invocation)
    {
        this.invocation = invocation;
        this.setText("Send to AWS");
        //Create sub menu
        sqlClick = new  JMenuItem("SQL injection");
        xssClick = new  JMenuItem("Cross Site Scripting");
        fileClick = new  JMenuItem("File Inclusion");
        //Add event
        SQLActionListener sqlAction = new SQLActionListener();
        sqlAction.toolFlag = invocation.getToolFlag();
        sqlClick.addActionListener(sqlAction);

        //Add sub menu
        this.add(sqlClick);
        this.add(xssClick);
        this.add(fileClick);
    }
    class SQLActionListener implements ActionListener {
        public int toolFlag;
        @Override
        public void actionPerformed(ActionEvent e) {
            
            System.out.println(this.toolFlag);
        }
    }
 
}

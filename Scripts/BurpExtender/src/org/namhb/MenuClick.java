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
    public JMenuItem sqlClick, xssClick, parameterManipulationClick, fileUploadClick, textSearchClick;
    public IHttpRequestResponse ihrr;
    public IHttpRequestResponse messageinfo;
    public int toolFlag;
    public Gui jPanel1;
    public MenuClick(IHttpRequestResponse ihrr, Gui jPanel1)
    {
        this.ihrr = ihrr;
        this.toolFlag = jPanel1.getLogEntrySize();
        this.jPanel1 = jPanel1;
        this.setText("Send to AWS");
        //Create sub menu
        sqlClick = new  JMenuItem("SQL injection");
        xssClick = new  JMenuItem("Cross Site Scripting");
        parameterManipulationClick = new  JMenuItem("Parameter Manipulation");
        fileUploadClick = new  JMenuItem("File Upload");
        textSearchClick = new  JMenuItem("Text Search");
        //Add event
        SQLActionListener sqlAction = new SQLActionListener();
        sqlClick.addActionListener(sqlAction);
        XssActionListener xssAction = new XssActionListener();
        xssClick.addActionListener(xssAction);
        ParameterManipulationActionListener parameterManipulationAction = new ParameterManipulationActionListener();
        parameterManipulationClick.addActionListener(parameterManipulationAction);
        FileUploadActionListener fileUploadAction = new FileUploadActionListener();
        fileUploadClick.addActionListener(fileUploadAction);
        TextSearchActionListener textSearchAction = new TextSearchActionListener();
        textSearchClick.addActionListener(textSearchAction);
        //Add sub menu
        this.add(sqlClick);
        this.add(xssClick);
        this.add(parameterManipulationClick);
        this.add(fileUploadClick);
        this.add(textSearchClick);
    }
    class SQLActionListener implements ActionListener {
        @Override
        public void actionPerformed(ActionEvent e) {
            //Add to list
            jPanel1.addRowDataModel(toolFlag, ihrr, "SQL injection");
        }
    }
    class XssActionListener implements ActionListener {
        @Override
        public void actionPerformed(ActionEvent e) {
            //Add to list
            jPanel1.addRowDataModel(toolFlag, ihrr, "Cross Site Sripting");
        }
    }
    class ParameterManipulationActionListener implements ActionListener {
        @Override
        public void actionPerformed(ActionEvent e) {
            //Add to list
            jPanel1.addRowDataModel(toolFlag, ihrr, "Parameter Manipulation");
        }
    }
    class FileUploadActionListener implements ActionListener {
        @Override
        public void actionPerformed(ActionEvent e) {
            //Add to list
            jPanel1.addRowDataModel(toolFlag, ihrr, "File Upload");
        }
    }
    class TextSearchActionListener implements ActionListener {
        @Override
        public void actionPerformed(ActionEvent e) {
            //Add to list
            jPanel1.addRowDataModel(toolFlag, ihrr, "Text Search");
        }
    }
 
}

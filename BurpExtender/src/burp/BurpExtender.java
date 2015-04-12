package burp;

import java.awt.Component;
import java.awt.BorderLayout;
import javax.swing.*;
import javax.swing.BoxLayout;
import net.miginfocom.layout.*;
import net.miginfocom.swing.*;
import burp.MainLayout;
import java.awt.Button;
import java.awt.Color;
import java.awt.Dimension;
import java.awt.Label;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import javax.swing.table.AbstractTableModel;
import javax.swing.table.TableModel;
public class BurpExtender implements IBurpExtender, ITab
{
    private IBurpExtenderCallbacks callbacks;
    private Gui jPanel1;
    @Override
    public void registerExtenderCallbacks(final IBurpExtenderCallbacks callbacks)
    {
        // your extension code here
        callbacks.setExtensionName("NamHB Extension");
        SwingUtilities.invokeLater(new Runnable() {
            @Override
            public void run(){
                // table of log entries
                jPanel1 = new Gui();
                callbacks.addSuiteTab(BurpExtender.this);
            }
        });
    }
    @Override
    public String getTabCaption () {
        return "Extension" ;
    }
    @Override
    public Component getUiComponent () {
        return  jPanel1;
    }

}

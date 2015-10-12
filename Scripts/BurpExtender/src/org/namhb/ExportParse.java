/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package org.namhb;
import java.io.File;
import java.util.ArrayList;
import java.util.List;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.parsers.DocumentBuilderFactory;
import org.w3c.dom.Document;
import org.w3c.dom.Element;
import org.w3c.dom.Node;
import org.w3c.dom.NodeList;
/**
 *
 * @author habachnam
 */
public class ExportParse {
    public List<ResultEntry> resultList = new ArrayList<ResultEntry>();
    public String exportFilePath = "";
    public ExportParse(String exportFilePath)
    {
        this.exportFilePath = exportFilePath;
        try {
            File inputFile = new File(exportFilePath);
            DocumentBuilderFactory dbFactory = DocumentBuilderFactory.newInstance();
            DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
            Document doc = dBuilder.parse(inputFile);
            doc.getDocumentElement().normalize();
            Element root = doc.getDocumentElement();
            // lay danh sach node con cua 1 node
            NodeList nodeListScanGroup = root.getChildNodes();
            printNoteWithParam(nodeListScanGroup, "ReportItems");

        } catch (Exception e) {
            e.printStackTrace();
        }
    }
    public List<ResultEntry> getResult()
    {
        return resultList;
    }
    public String generateHTML()
    {
        String htmlString = "<html>"
                + "<b>Vulnerability description:</b><br/>"
                + "<table border=\"1\"><tr><td>Name</td><td>Severity</td><td>Parameter</td><td>Affects</td><td>Details</td></tr>";
        for(int count = 0; count < resultList.size(); count++)
        {
            ResultEntry entry = resultList.get(count);
            String tmp = String.format("<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>", 
                    entry.Name,
                    entry.Severity,
                    entry.Parameter,
                    entry.Affects,
                    entry.Details
                    );
            htmlString = htmlString + tmp;
        }
        htmlString = htmlString + "</table></html>";
        return htmlString;
    }
    public void printNoteWithParam(NodeList nodeList, String str) {
        for (int count = 0; count < nodeList.getLength(); count++) {
            Node tempNode = nodeList.item(count);
            // make sure it's element node.
            if ((tempNode.getNodeType() == Node.ELEMENT_NODE)) {
                if (tempNode.getNodeName().equals(str)) {                 
                    Element eScan = (Element) tempNode;
                    NodeList nodeListEScan = eScan.getChildNodes();
                    printNoteGetSeverity(nodeListEScan);
                    break;
                }
            }
            if (tempNode.hasChildNodes()) {
                // loop again if has child nodes
                printNoteWithParam(tempNode.getChildNodes(), str);
            }
            
        }
    }
    public void printNoteGetSeverity(NodeList nodeList) {
        ResultEntry resultItem = new ResultEntry();
        for (int count = 0; count < nodeList.getLength(); count++) 
        {
            Node tempNode = nodeList.item(count);
            // make sure it's element node.
            if (tempNode.getNodeType() == Node.ELEMENT_NODE) {
                // get node name and value
                if (tempNode.getNodeName().equalsIgnoreCase("Name")) {
                    resultItem.Name = tempNode.getTextContent();
                }
                if (tempNode.getNodeName().equalsIgnoreCase("Severity")) {
                    resultItem.Severity = tempNode.getTextContent();
                }
                if (tempNode.getNodeName().equalsIgnoreCase("Details")) {
                    resultItem.Details = tempNode.getTextContent();
                }
                if (tempNode.getNodeName().equalsIgnoreCase("Parameter")) {
                    resultItem.Parameter = tempNode.getTextContent();
                }
                if (tempNode.getNodeName().equalsIgnoreCase("Request")) {
                    resultItem.Request = tempNode.getTextContent();
                }
                if (tempNode.getNodeName().equalsIgnoreCase("Response")) {
                    resultItem.Response = tempNode.getTextContent();
                }
                if (tempNode.getNodeName().equalsIgnoreCase("Affects")) {
                    resultItem.Affects = tempNode.getTextContent();
                }
                if (tempNode.hasChildNodes()) {
                    // loop again if has child nodes
                    printNoteGetSeverity(tempNode.getChildNodes());
                }
                
            }
        }
        if(resultItem.Name != null)
        {
            System.out.println(resultItem.Name);
            resultList.add(resultItem);
        }
    }
}

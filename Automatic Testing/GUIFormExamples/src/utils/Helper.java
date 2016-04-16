/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package utils;
import FSM_GRAPH.FSM;
import htmlElement.ListElementStatus;
import htmlElement.WebElements;
import java.awt.Component;
import javax.swing.JFileChooser;
import utils.Logger;
import jxl.Sheet;
import jxl.Workbook;
import jxl.write.*;
import java.io.*;  
import java.text.MessageFormat;
import java.util.ArrayList;
import java.util.HashSet;
import javax.swing.JLabel;
import javax.swing.filechooser.FileNameExtensionFilter;
import javax.swing.table.DefaultTableModel;
import javax.swing.table.TableModel;
import javax.xml.parsers.DocumentBuilderFactory;
import javax.xml.parsers.DocumentBuilder;
import javax.xml.xpath.XPath;
import javax.xml.xpath.XPathConstants;
import javax.xml.xpath.XPathExpression;
import javax.xml.xpath.XPathExpressionException;
import javax.xml.xpath.XPathFactory;
import org.w3c.dom.Document;
import org.w3c.dom.NodeList;
import org.w3c.dom.Node;
import org.w3c.dom.Element;


/**
 *
 * @author namhb
 */
public class Helper {
    JFileChooser chooser = new JFileChooser();
    DefaultTableModel elementmodel, stateModel, transactionModel, eventModel, valueModel;
    TableModel elementTableModel, stateTableModel, transactionTableModel, eventTableModel, valueTableModel;
    Logger logger;
    WebDriver webDriver;
    FSM fsm;
    Functions functions;
    public Helper(Logger logger)
    {
        this.logger = logger;
        this.webDriver = new WebDriver(this.logger);
        this.functions = new Functions();
    }
    public void setElementTableModel(TableModel elementTableModel)
    {
        this.elementTableModel = elementTableModel;
        this.elementmodel = (DefaultTableModel) this.elementTableModel;
    }
    public void setValueTableModel(TableModel valueTableModel)
    {
        this.valueTableModel = valueTableModel;
        this.valueModel = (DefaultTableModel) this.valueTableModel;
    }
    public void setStateTableModel(TableModel stateTableModel)
    {
        this.stateTableModel = stateTableModel;
        this.stateModel = (DefaultTableModel) this.stateTableModel;
    }
    public void setTransactionTableModel(TableModel transactionTableModel)
    {
        this.transactionTableModel = transactionTableModel;
        this.transactionModel = (DefaultTableModel) this.transactionTableModel;
    }
    public void setEventTableModel(TableModel eventTableModel)
    {
        this.eventTableModel = eventTableModel;
        this.eventModel = (DefaultTableModel) this.eventTableModel;
    }
    public void import2WebDriver()
    {
        this.webDriver.import2WebDriver(this.elementmodel, this.stateModel, this.transactionModel, this.eventModel, this.valueModel);
//        fsm = new FSM(numOfTest, this.name, stateList, transitionList, beginState, endStateList);
    }
    public Document xmlParse(String filePath)
    {
        try {
            File inputFile = new File(filePath);
            DocumentBuilderFactory dbFactory  = DocumentBuilderFactory.newInstance();
            DocumentBuilder dBuilder = dbFactory.newDocumentBuilder();
            Document doc = dBuilder.parse(inputFile);
            doc.getDocumentElement().normalize();
            return doc;
        }
        catch(Exception e)
        {
            this.logger.error("Read file error");
            this.logger.error(e.toString());
            return null;
        }
    }
    public void getAllEvent(Document doc) throws XPathExpressionException
    {
        int stateIDFrom, stateIDTo, eventID;
        String input, htmlID, action;
        XPath xpath;
        XPathExpression expr;
        NodeList nl;
        xpath = XPathFactory.newInstance().newXPath();
        HashSet<String> eventArray = new HashSet<String>();
        // Get all fsa_trans
        expr = xpath.compile("//fsa_trans");
        nl = (NodeList)expr.evaluate(doc, XPathConstants.NODESET);
        this.logger.debug(MessageFormat.format("Number of  fsa_trans {0}", nl.getLength()));
        for (int temp = 0; temp < nl.getLength(); temp++) {
            Node nNode = nl.item(temp);
            if (nNode.getNodeType() == Node.ELEMENT_NODE) {
                Element eElement = (Element) nNode;
                input = eElement.getElementsByTagName("input").item(0).getTextContent();
                Element eElementFrom = (Element) eElement.getElementsByTagName("from").item(0);              
                stateIDFrom = Integer.parseInt(eElementFrom.getElementsByTagName("id").item(0).getTextContent());
                Element eElementTo = (Element) eElement.getElementsByTagName("to").item(0);
                stateIDTo = Integer.parseInt(eElementTo.getElementsByTagName("id").item(0).getTextContent());
                this.logger.debug(MessageFormat.format("Event {0} from {1} to {2}", input, stateIDFrom, stateIDTo));
                // Update transaction table
                this.transactionModel.setValueAt(input, stateIDFrom, stateIDTo+2);
                // Add to event list
                eventArray.add(input);
            }
        }
        eventID = 0;
        this.logger.debug(MessageFormat.format("Number of  Events {0}", eventArray.size()));
        for (String str : eventArray) {
            if(this.functions.checkCond(str))
                str = this.functions.getNameEvent(str);
            htmlID = this.functions.getHTMLIdOfEvent(str);
            action = this.functions.getActionOfEvent(str);
            this.logger.debug(MessageFormat.format("Event id {0}: {1}", eventID, str));
            this.eventModel.addRow(new Object[] {eventID, str, htmlID, action});
            eventID +=1;
        }
    }
    public void getAllStates(Document doc) throws XPathExpressionException
    {
        //Get all states name
        String stateName, noteValue;
        String stateX, stateY, noteX, noteY;
        int stateID;
        XPath xpath;
        XPathExpression expr;
        NodeList nl;
        xpath = XPathFactory.newInstance().newXPath();
        expr = xpath.compile("//structure[@type=\"state_set\"]/state");
        nl = (NodeList)expr.evaluate(doc, XPathConstants.NODESET);
        this.logger.debug(MessageFormat.format("Number of States {0}", nl.getLength()));
        for (int temp = 0; temp < nl.getLength(); temp++) {
            Node nNode = nl.item(temp);
            if (nNode.getNodeType() == Node.ELEMENT_NODE) {
                Element eElement = (Element) nNode;
                stateName = eElement.getElementsByTagName("name").item(0).getTextContent();
                stateID = Integer.parseInt(eElement.getElementsByTagName("id").item(0).getTextContent());
                this.logger.debug(MessageFormat.format("ID: {0}, Name: {1}", stateID, stateName));
                // Add to table
                this.stateModel.addRow(new Object[]{ stateID, 5, stateName});
                // Add Row to transaction
                this.transactionModel.addRow(new Object[] {stateID, stateName});
                // Add columns to transaction
                this.transactionModel.addColumn(stateName);
            }
        }
        //Find Start states
        expr = xpath.compile("//structure[@type=\"start_state\"]/state");
        nl = (NodeList)expr.evaluate(doc, XPathConstants.NODESET);
        this.logger.debug(MessageFormat.format("Number of Start States {0}", nl.getLength()));
        for (int temp = 0; temp < nl.getLength(); temp++) {
            Node nNode = nl.item(temp);
            if (nNode.getNodeType() == Node.ELEMENT_NODE) {
                Element eElement = (Element) nNode;
                stateName = eElement.getElementsByTagName("name").item(0).getTextContent();
                stateID = Integer.parseInt(eElement.getElementsByTagName("id").item(0).getTextContent());
                this.logger.debug(MessageFormat.format("Start states - ID: {0}, Name: {1}", stateID, stateName));
                // Update states to table
                this.stateModel.setValueAt(0, stateID, 1);
            }
        }
        //Find Final state
        expr = xpath.compile("//structure[@type=\"final_states\"]/state");
        nl = (NodeList)expr.evaluate(doc, XPathConstants.NODESET);
        this.logger.debug(MessageFormat.format("Number of Start States {0}", nl.getLength()));
        for (int temp = 0; temp < nl.getLength(); temp++) {
            Node nNode = nl.item(temp);
            if (nNode.getNodeType() == Node.ELEMENT_NODE) {
                Element eElement = (Element) nNode;
                stateName = eElement.getElementsByTagName("name").item(0).getTextContent();
                stateID = Integer.parseInt(eElement.getElementsByTagName("id").item(0).getTextContent());
                this.logger.debug(MessageFormat.format("Final states - ID: {0}, Name: {1}", stateID, stateName));
                // Update states to table
                this.stateModel.setValueAt(1, stateID, 1);
            }
        }
        //Get all X, Y
        ArrayList<ArrayList<String>> allstatePoint = new ArrayList<ArrayList<String>>();
        
        String statePointData;
        expr = xpath.compile("//state_point");
        nl = (NodeList)expr.evaluate(doc, XPathConstants.NODESET);
        this.logger.debug(MessageFormat.format("Number of State Point {0}", nl.getLength()));
        for (int temp = 0; temp < nl.getLength(); temp++) {
            Node nNode = nl.item(temp);
            if (nNode.getNodeType() == Node.ELEMENT_NODE) {
                Element eElement = (Element) nNode;
                stateID = Integer.parseInt(eElement.getElementsByTagName("state").item(0).getTextContent());
                Element eElementPoint = (Element) eElement.getElementsByTagName("point").item(0);
                stateX = eElementPoint.getElementsByTagName("x").item(0).getTextContent();
                stateY = eElementPoint.getElementsByTagName("y").item(0).getTextContent();
                this.logger.debug(MessageFormat.format("States Point - ID: {0}, X: {1}, Y: {2}", stateID, stateX, stateY));
                // Update point x,y to table
                this.stateModel.setValueAt(stateX, stateID, 3);
                this.stateModel.setValueAt(stateY, stateID, 4);
                statePointData = MessageFormat.format("{0}|{1}|{2}", Integer.toString(stateID), stateX, stateY);
                ArrayList al = new ArrayList();
                al.add(Integer.toString(stateID));
                al.add(stateX);
                al.add(stateY);
                allstatePoint.add(al);
            }
        }
        //Get all element of state
        expr = xpath.compile("//note");
        nl = (NodeList)expr.evaluate(doc, XPathConstants.NODESET);
        this.logger.debug(MessageFormat.format("Number of Note {0}", nl.getLength()));
        for (int temp = 0; temp < nl.getLength(); temp++) {
            Node nNode = nl.item(temp);
            if (nNode.getNodeType() == Node.ELEMENT_NODE) {
                Element eElement = (Element) nNode;
                Element eElementPoint = (Element) eElement.getElementsByTagName("point").item(0);
                noteValue = eElement.getElementsByTagName("value").item(0).getTextContent();
                stateX = eElementPoint.getElementsByTagName("x").item(0).getTextContent();
                stateY = eElementPoint.getElementsByTagName("y").item(0).getTextContent();
                this.logger.debug(MessageFormat.format("Note Point - Value: {0}, X: {1}, Y: {2}", noteValue, stateX, stateY));
                int id = this.findIdByPoint(allstatePoint, stateX, stateY);
                if(id < 0)
                {
                    this.logger.debug("Note not for State");
                }
                else
                {
                    // Update value
                    String[] tmp = noteValue.split(",");
                    for (int temp2 = 0; temp2 < tmp.length; temp2++)
                    {
                        this.logger.debug(MessageFormat.format("States id {0} have Element id {1}", id, tmp[temp2]));
                        this.stateModel.setValueAt("o", id, Integer.parseInt(tmp[temp2])+5);
                    }
                }
            }
        }
    }
    public int findIdByPoint(ArrayList<ArrayList<String>> allstatePoint, String stateX, String stateY)
    {
        ArrayList statePoint;
        String alstateX, alstateY;
        for (int temp = 0; temp < allstatePoint.size(); temp++)
        {
            alstateX = allstatePoint.get(temp).get(1);
            alstateY = allstatePoint.get(temp).get(2);
            if((alstateX.equals(stateX)) && (alstateY.equals(stateY)))
            {
                return Integer.parseInt(allstatePoint.get(temp).get(0));
            }
        }
        return -1;
    }
    public void selectJFlapFile(Component parent)
    {
        if(this.elementmodel != null)
        {
            chooser.setFileFilter(new FileNameExtensionFilter("JFLAP Files", "jflap"));
            int returnVal = chooser.showOpenDialog(parent);
            if(returnVal == JFileChooser.APPROVE_OPTION) {
                this.logger.debug("Openning JFLAP file: " + chooser.getSelectedFile().getAbsolutePath());
                this.processJFlapFile(chooser.getSelectedFile().getAbsolutePath());
            }
        }
        else
        {
            this.logger.error("Select Element file first!");
        }
    }
    public void processJFlapFile(String filePath)
    {
        Document doc = this.xmlParse(filePath);
        if(doc != null)
        {
            try
            {
                this.getAllStates(doc);
                this.getAllEvent(doc);
            }
            catch(Exception e)
            {
                this.logger.error("Read file error");
                this.logger.error(e.toString());
            }
        }
    }
    public void selectExcelFile(Component parent, JLabel elementCountLabel)
    {
        chooser.setFileFilter(new FileNameExtensionFilter("Excel Files", "xls"));
        int returnVal = chooser.showOpenDialog(parent);
        if(returnVal == JFileChooser.APPROVE_OPTION) {
            this.logger.debug("Openning Excel file: " + chooser.getSelectedFile().getAbsolutePath());
            this.processElementExcelFile(chooser.getSelectedFile().getAbsolutePath(), elementCountLabel);
        }        
    }
    public void displayElementExcelFile()
    {
        
    }
    public void processElementExcelFile(String filePath, JLabel elementCountLabel)
    {
        try
        {
            Workbook workbook = Workbook.getWorkbook(new java.io.File(filePath));
            Sheet sheet = workbook.getSheet(0);
            int nelem = Integer.valueOf(sheet.getCell(0, 0).getContents().trim()).intValue();
            int numOfTest = Integer.valueOf(sheet.getCell(4, 0).getContents().trim()).intValue();
            this.logger.debug(MessageFormat.format("Number of Element {0}", nelem));
            this.logger.debug(MessageFormat.format("Number of Test value {0}", numOfTest));
            // Add to value table
            for (int i=0; i<numOfTest; i++){
                this.valueModel.addColumn(i+1);
            }
            elementCountLabel.setText(Integer.toString(nelem));
            this.logger.debug("Start read Element");
            for (int i=0; i<nelem; i++){
        	int id = Integer.valueOf(sheet.getCell(1, i+2).getContents().trim()).intValue();
        	String html_id = sheet.getCell(2, i+2).getContents().trim();
        	String type = sheet.getCell(3, i+2).getContents().trim();
        	this.logger.debug(MessageFormat.format("ID: {0}, HTML id: {1}, Type: {2}", id, html_id, type));
                // Add Row               
                this.elementmodel.addRow(new Object[]{ id, html_id, type});
                // Add Column to state table                
                this.stateModel.addColumn(id);
                // Add Row to value
                this.valueModel.addRow(new Object[]{ id, html_id});
                // For old code, get value, add to value table
                ArrayList<String> values = new ArrayList<String>();
        	for (int j=0; j<numOfTest; j++){
        		String tvalue = sheet.getCell(4+j, i+2).getContents().trim();
        		if (tvalue.length()==0){
                            tvalue = "";
        		}
                        else
                        {
                            this.logger.debug(MessageFormat.format("Add value: {0}", tvalue));
                        }
                        this.valueModel.setValueAt(tvalue, id, j+2);
        		values.add(tvalue);
        	}
            }
        }
        catch(Exception e)
        {
            this.logger.error("Read file error");
            this.logger.error(e.toString());
        }

    }
}

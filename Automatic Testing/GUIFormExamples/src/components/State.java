package components;

import arg.*;
import java.io.PrintWriter;
import java.io.StringWriter;

import htmlElement.ListWebElements;
import htmlElement.ElementStatus;
import htmlElement.ListElementStatus;
import htmlElement.WebElements;
import java.text.MessageFormat;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;
import org.openqa.selenium.support.ui.Select;
import java.text.MessageFormat;

import utils.*;
public class State {

    public int id;
    public String name;
    public ListElementStatus listElementStatus; // for this state
    public ListWebElements listWebElements;
    public Functions functions;
    public State() {
        
    }

    public void setId(int id) {
        this.id = id;
    }

    public int getId() {
        return id;
    }

    public State(int _id, String _name, ListElementStatus _listElementStatus, ListWebElements _listWebElements) {
        id = _id;
        name = _name;
        listElementStatus = _listElementStatus;
        listWebElements = _listWebElements;
    }

    public State(String _name, ListElementStatus _elem_st_list, ListWebElements _elem_html_list) {
        name = _name;
        listElementStatus = _elem_st_list;
        listWebElements = _elem_html_list;
    }

    public String getName() {
        return name;
    }

    public void printState(utils.Logger logger) {
        
        logger.debug("PRINT STATE: " + name);
        for (int i = 0; i < listWebElements.getSize(); i++) {
            logger.debug(MessageFormat.format("{0}/{1}",listWebElements.getElementByIndex(i).getHtml_id(), listElementStatus.getElementByIndex(i).getStatus()));
        }
    }

    public void addMoreInfo(String _name, ListElementStatus _elem_st_list, ListWebElements _elem_html_list) {

        if (name.equals(_name)) {
            for (int i = 0; i < _elem_html_list.getSize(); i++) {
                listWebElements.addElement(_elem_html_list.getElementByIndex(i));
                listElementStatus.addElement(_elem_st_list.getElementByIndex(i));
            }

        }
    }

    public String getStringFromHtmlById(WebElement webelem, WebElements eh, int test_current) {
        try {
            String value = "";
            if (eh.getType().compareTo(ElementType.TEXTBOX) == 0) {
                value = webelem.getAttribute(WebdriverGetAttribute.ATT_VALUE);
            } else if (eh.getType().compareTo(ElementType.CHECKBOX) == 0) {
                if (webelem.isSelected()) {
                    value = "1";
                } else {
                    value = "0";
                }
            } else if (eh.getType().compareTo(ElementType.RADIO) == 0) {
                if (webelem.isSelected()) {
                    value = "1";
                } else {
                    value = "0";
                }
            } else if (eh.getType().compareTo(ElementType.LISTBOX) == 0) {
                Select clickThis = new Select(webelem);
                clickThis.selectByValue(eh.getValueAt(test_current));
                value = eh.getValueAt(test_current);
            } else {
                value = webelem.getText();
            }

            return value;
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }

    }

	// test_current la bien chi xem test lan thu may, tuong ung voi bo gia tri nao
    public boolean checkState(WebDriver driver, int test_current, utils.Logger logger) {
        try {
            for (int i = 0; i < listElementStatus.getSize(); i++) {
                ElementStatus e = listElementStatus.getElementByIndex(i);
                if (e.getStatus().compareTo(ElementStatusValue.IGNORE) == 0) {
                    continue;
                }
                WebElements eh = listWebElements.getElementById(e.getId());
                if (eh.getValueAt(test_current).compareTo(ElementStatusValue.IGNORE) == 0) {
                    continue;
                }
                WebElement webelem;
                this.functions = new Functions();
                String selectBy = this.functions.getSelectType(eh.getHtml_id());
                String selectValue = this.functions.getSelectValue(eh.getHtml_id());
                
                if (selectBy.toLowerCase().compareTo(WebDriverSelectType.NAME.toLowerCase()) == 0) {
                    webelem = driver.findElement(By.name(selectValue));
                } else if (selectBy.toLowerCase().compareTo(WebDriverSelectType.ID.toLowerCase()) == 0) {
                    webelem = driver.findElement(By.id(selectValue));
                } else if (selectBy.toLowerCase().compareTo(WebDriverSelectType.CLASS.toLowerCase()) == 0) {
                    webelem = driver.findElement(By.className(selectValue));
                } else if (selectBy.toLowerCase().compareTo(WebDriverSelectType.XPATH.toLowerCase()) == 0) {
                    webelem = driver.findElement(By.xpath(selectValue));
                } else if (selectBy.toLowerCase().compareTo(WebDriverSelectType.TAG.toLowerCase()) == 0) {
                    webelem = driver.findElement(By.tagName(selectValue));
                } else {
                    webelem = driver.findElement(By.id(selectValue)); // Default by id
                }  
                String value = getStringFromHtmlById(webelem, eh, test_current);
                if (e.getStatus().compareTo(ElementStatusValue.EMPTY) == 0) {
                    if (value.length() != 0) {
                        logger.debug("Fail at F1, ElementStatusValue.EMPTY");
                        return false;
                    }
                } else if (e.getStatus().compareTo(ElementStatusValue.DEFAULT) == 0) {
                    if (value.compareTo(eh.getValueAt(test_current)) != 0) {
                        logger.debug("Fail at F2, ElementStatusValue.DEFAULT. Wrong value");
                        logger.debug(MessageFormat.format("Real Output: {0} \t and Expected Output: {1} of element: {2} are different", value, eh.getValueAt(test_current), eh.getHtml_id()));
                        if (eh.getValueAt(test_current).compareTo(ElementStatusValue.IGNORE) == 0) {
                            continue;
                        }
                        return false;
                    }
                } else if (value.compareTo(e.getStatus()) != 0) {
                    logger.debug("Fail at F3");
                    logger.debug(MessageFormat.format("Strings not compare: {0} of element {1} has status {2}",value, eh.getHtml_id(),e.getStatus()));
                    return false;
                }
            }
            return true;
        } catch (Exception e) {
            logger.debug("Check Fail. Cannot match HTML element");
            return false;
        }
    }
    public void setName(String name) {
        this.name = name;
    }

    public static String getStackTrace(final Throwable throwable) {
        final StringWriter sw = new StringWriter();
        final PrintWriter pw = new PrintWriter(sw, true);
        throwable.printStackTrace(pw);
        return sw.getBuffer().toString();
    }

}

package components;

import htmlElement.ListWebElements;
import htmlElement.WebElements;

import org.openqa.selenium.By;
import org.openqa.selenium.WebDriver;
import org.openqa.selenium.WebElement;

import arg.*;
import java.text.MessageFormat;
import utils.*;

public class Event {

    public String name;
    public String html_id;
    public String action;
    public Functions functions;
    ListWebElements listElement;

    public Event(String _name, String _html_id, String _action, ListWebElements _listElement) {
        name = _name;
        html_id = _html_id;
        action = _action;
        listElement = _listElement;
        functions = new Functions();
    }

    public void doEvent(WebDriver driver, int test_current, utils.Logger logger) {
        try {

            WebElements elem = listElement.getElementByName(html_id);
            WebElement webelem;

            String selectBy = this.functions.getSelectType(elem.getHtml_id());
            String selectValue = this.functions.getSelectValue(elem.getHtml_id());
            if (selectBy.toLowerCase().compareTo(WebDriverSelectType.NAME.toLowerCase()) == 0) {
                webelem = driver.findElement(By.name(selectValue));
            } else if (selectBy.toLowerCase().compareTo(WebDriverSelectType.ID.toLowerCase()) == 0) {
                webelem = driver.findElement(By.id(selectValue));
            } else if (selectBy.toLowerCase().compareTo(WebDriverSelectType.CLASS.toLowerCase()) == 0) {
                webelem = driver.findElement(By.className(selectValue));
            } else if (selectBy.toLowerCase().compareTo(WebDriverSelectType.XPATH.toLowerCase()) == 0) {
                webelem = driver.findElement(By.xpath(selectValue));
            } else webelem = driver.findElement(By.id(selectValue)); // Default by id

            if (this.action.toLowerCase().compareTo(WebdriverActionType.ADDTEXT.toLowerCase()) == 0) {
                logger.debug(MessageFormat.format("Selected {0} by {1}. Add text: {2}",selectValue, selectBy, elem.getValueAt(test_current)));
                webelem.sendKeys(elem.getValueAt(test_current));
            } else if (this.action.toLowerCase().compareTo(WebdriverActionType.DELTEXT.toLowerCase()) == 0) {
                logger.debug(MessageFormat.format("Selected {0} by {1}. Clear text",selectValue, selectBy));
                webelem.clear();
            } else if (this.action.toLowerCase().compareTo(WebdriverActionType.CLICK.toLowerCase()) == 0) {
                logger.debug(MessageFormat.format("Selected {0} by {1}. Click",selectValue, selectBy));
                webelem.click();
            } else if (this.action.toLowerCase().compareTo(WebdriverActionType.SELECT.toLowerCase()) == 0) {
                logger.debug(MessageFormat.format("Selected {0} by {1}. Click",selectValue, selectBy));
                webelem.click();
            }

        } catch (Exception e) {
            e.printStackTrace();

        }

    }

    //Getter & Setter
    public String getName() {
        return name;
    }

    public String getAction() {
        return action;
    }

    public void setName(String name) {
        this.name = name;
    }

}

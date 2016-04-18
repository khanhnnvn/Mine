/*
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */
package utils;

import components.Condition;

/**
 *
 * @author habachnam
 */
public class Functions {
    
    public String getSelectType(String input)
    {
        // Lay type: name, id, xpath, class
        String temp = "";
        if (input.indexOf(":") >= 0) {
            temp = input.substring(0, input.indexOf(":"));
        } else {
            temp = input;
        }
        return temp;
    }
    public String getSelectValue(String input)
    {
        // Lay value sau : name, id, xpath, class
        String temp = "";
        if (input.indexOf(":") >= 0) {
            temp = input.substring(input.indexOf(":")+1, input.length());
        } else {
            temp = input;
        }
        return temp;
    }
    public String getNameEvent(String input) {
        // Lay event
        String temp = "";
        if (input.indexOf("}") >= 0) {
            temp = input.substring(input.indexOf("}") + 1, input.length());
        } else {
            temp = input;
        }
        return temp;
    }

    public boolean checkCond(String input) {
        int moNgoac = input.indexOf("{");
        int dongNgoac = input.indexOf("}");
        if (moNgoac >= 0 && dongNgoac > moNgoac) {
            return true;
        } else {
            return false;
        }
    }

    public Condition getCond(String input) {
        // {id/value}
        // Lay trong dau ngoac, tach biet bang /
        int moNgoac = input.indexOf("{");
        int dongNgoac = input.indexOf("}");
        String conds = "";
        Condition conditions;
        if (moNgoac >= 0 && dongNgoac > moNgoac) {
            conds = input.substring(moNgoac + 1, dongNgoac);
            int gachCheo = conds.indexOf("/");
            String id = conds.substring(0, gachCheo);
            String values = conds.substring(gachCheo + 1, conds.length());
            conditions = new Condition(id, values);
        } else {
            conditions = new Condition();
        }
        return conditions;
    }

    public String getHTMLIdOfEvent(String input) {
        String temp = "";
        if (input.indexOf(".") >= 0) {
            temp = input.substring(0, input.indexOf("."));
        } else {
            temp = input;
        }
        return temp;
    }

    public String getActionOfEvent(String input) {
        String temp = "";
        if (input.indexOf(".") >= 0) {
            temp = input.substring(input.indexOf(".") + 1, input.length());
        } else {
            temp = input;
        }
        return temp;
    }
}

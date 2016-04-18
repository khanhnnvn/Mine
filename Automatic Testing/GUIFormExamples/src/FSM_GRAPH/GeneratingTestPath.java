package FSM_GRAPH;

import java.text.MessageFormat;
import java.util.ArrayList;
import utils.*;

public class GeneratingTestPath {

    boolean[][] isUsed;
    String[][] nameTransition;
    ArrayTransList[][] arrTranLists;
    int numberStates;
    ArrayList<Integer> listEndState;
    ArrayList<Integer> addMore;
    ArrayList<Integer> arrTemp;
    Logger logger;

    public GeneratingTestPath(FSM fsm, Logger logger) {
        arrTemp = new ArrayList<Integer>();
        listEndState = new ArrayList<Integer>();
        addMore = new ArrayList<Integer>();
        numberStates = fsm.getNumberOfState();
        this.logger = logger;
        this.logger.debug(MessageFormat.format("N = : {0}", numberStates));
        isUsed = new boolean[numberStates][];
        for (int i = 0; i < numberStates; i++) {
            isUsed[i] = new boolean[numberStates];
            for (int j = 0; j < numberStates; j++) {
                isUsed[i][j] = false;
            }
        }
        //arrTransition = null
        arrTranLists = new ArrayTransList[numberStates][];
        for (int i = 0; i < numberStates; i++) {
            arrTranLists[i] = new ArrayTransList[numberStates];
            for (int j = 0; j < numberStates; j++) {
                arrTranLists[i][j] = new ArrayTransList();
            }
        }
        //nameTransition = null
        nameTransition = new String[numberStates][];
        for (int i = 0; i < numberStates; i++) {
            nameTransition[i] = new String[numberStates];
            for (int j = 0; j < numberStates; j++) {
                nameTransition[i][j] = "";
            }
        }
        for (int i = 0; i < fsm.getNumberOfTransition(); i++) {
            int a = fsm.getIndexBeginStateOfTransition(i);
            int b = fsm.getIndexEndStateOfTransition(i);
            nameTransition[a][b] = fsm.getNameOfTransitioin(i);
            isUsed[a][b] = false;
            arrTranLists[a][b].Add(fsm.getNameOfTransitioin(i));
        }
        for (int i = 0; i < fsm.getSizeOfEndStateList(); i++) {
            String tempName = fsm.getNameEndStateByIndex(i);
            for (int j = 0; j < numberStates; j++) {
                if (tempName.equals(fsm.getNameStateByIndex(j))) {
                    listEndState.add(j);
                }
            }
        }
        for (int i = 0; i < numberStates; i++) {
            for (int j = 0; j < numberStates; j++) {
                if (arrTranLists[i][j].getSize() > 0) {
                    String tmp = (i + "; " + j + ": " + arrTranLists[i][j].printAll());
                    this.logger.debug(tmp);
                }
            }
        }
        this.logger.debug("END STATE LIST:");
        for (int i = 0; i < listEndState.size(); i++) {
            this.logger.debug(listEndState.get(i).toString());
        }
    }

    //Xoa phan sort va add
    public ThePath automatedGeneratingTestPath() {
        ThePath PATH;
        PATH = new ThePath(this.logger);
        arrTemp.clear();
        arrTemp.add(0);
        DFS(0, PATH);
        addToPath(PATH);
        PATH.sort();
        PATH.printPath();
        printList();
        return PATH;
    }

    //Xoa phan danh dau dinh
    private void DFS(int i, ThePath PATH) {
        int t = 0;
        for (int j = 0; j < numberStates; j++) {
            if (arrTranLists[i][j].getSize() > 0 && isUsed[i][j] == false) {
                t++;
                //overState[j]=1;
                arrTranLists[i][j].RemoveHead();
                if (arrTranLists[i][j].IsEmpty()) {
                    isUsed[i][j] = true;
                }
                arrTemp.add(j);
                DFS(j, PATH);
                arrTemp.remove(arrTemp.size() - 1);
            }
        }
        if (t == 0) {
            PATH.Add(arrTemp);
        }
    }

    //Kiem tra
    public void printCheck() {
        this.logger.debug("CHECK DUYET");
        for (int i = 0; i < numberStates; i++) {
            for (int j = 0; j < numberStates; j++) {
                if (isUsed[i][j] != false) {
                    this.logger.debug( MessageFormat.format("[{0},{1}]{2}",i,j,isUsed[i][j]));
                }
            }
        }
    }

    //In chuoi bat dau tu mot vi tri i
    public void printList() {
        this.logger.debug("Chuoi sau khi them");
        String tmp="";
        for (int j = 0; j < addMore.size(); j++) {
            tmp = MessageFormat.format("{0} {1}", tmp, addMore.get(j));
        }
        this.logger.debug(tmp);
    }

    public void addToPath(ThePath PATH) {
        for (int i = 0; i < PATH.getSize(); i++) {
            if (!inEndStateList(PATH.getLastElemFromPathNumber(i), listEndState)) {
                this.logger.debug(MessageFormat.format("i={0}", i));
                addToPathAfter(PATH.getLastElemFromPathNumber(i));
                for (int j = 0; j < addMore.size(); j++) {
                    PATH.getListByIndex(i).add(addMore.get(j));
                }
                while (!addMore.isEmpty()) {
                    addMore.remove(0);
                }
            }
        }
    }

    // Them state vao path
    public void addToPathAfter(int i) {
        if (inEndStateList(i, listEndState) == true) {
            return;
        }
        for (int j = 0; j < numberStates; j++) {
            if (nameTransition[i][j].length() > 0 && isUsed[i][j] == true) {
                isUsed[i][j] = false;
                addMore.add(j);
                this.logger.debug( MessageFormat.format("[IAM HERE: {0}",j));
                addToPathAfter(j);
                break;
            }
        }
    }

    public boolean inEndStateList(int gt, ArrayList<Integer> listInt) {
        for (int i = 0; i < listInt.size(); i++) {
            if (gt == listInt.get(i)) {
                return true;
            }
        }
        return false;
    }
}

class ArrayTransList {

    ArrayList<String> arrList;

    public ArrayTransList() {
        // TODO Auto-generated constructor stub
        arrList = new ArrayList<String>();
    }

    public ArrayTransList(ArrayList<String> arrList) {
        this.arrList = arrList;
    }

    public void Add(String element) {
        arrList.add(element);
    }

    public void RemoveHead() {
        arrList.remove(0);
    }

    public boolean IsEmpty() {
        return arrList.isEmpty();
    }

    public String printAll() {
        String rs = "{";
        if (arrList.size() > 0) {
            for (int i = 0; i < arrList.size() - 1; i++) {
                rs += arrList.get(i) + ", ";
            }
            rs += arrList.get(arrList.size() - 1);
        }
        rs += "}";
        return rs;
    }

    public int getSize() {
        return arrList.size();
    }

    public String getByIndex(int i) {
        return arrList.get(i);
    }
}

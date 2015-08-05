@WebService(serviceName = "AuthenticationWS")
public class AuthenticationWS {

    @Resource
    private WebServiceContext wsContext;

    public boolean authentication(String username, String password) {

        MessageContext mc = wsContext.getMessageContext();
        HttpServletRequest request = (HttpServletRequest) mc.get(MessageContext.SERVLET_REQUEST);
        HttpSession session = request.getSession();

	        hashPassword = HASH(password);

	        Connection conn = Database.connect();
	        PrepareStatement stmt = conn.prepare("SELECT userid, username from user where username = "+username+" and password = "+hashPassword);

	        ResultSet rs = stmt.executeQuery();

        if (rs.next()) {
            session.invalidate();
            session = request.getSession();
            session.setAttribute("isAuthen", true);
            return true;
        } else {
            session.setAttribute("isAuthen", false);
            return false;
        }
    }

    private boolean isAuthen() {
        MessageContext mc = wsContext.getMessageContext();
        HttpServletRequest request = (HttpServletRequest) mc.get(MessageContext.SERVLET_REQUEST);
        HttpSession session = request.getSession();
        boolean isAuthen = (boolean) session.getAttribute("isAuthen");
        if (isAuthen) {
            return true;
        } else {
            return false;
        }
    }
    public int getCount(int count) {
        if (isAuthen()) {
            // OK, Let is go. 
            // Flag is xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
        } else {
            // Return Authentication Require
        }
    } 
}

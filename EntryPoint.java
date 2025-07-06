import py4j.Gateway;
import py4j.GatewayServer;

import java.util.List;

public class EntryPoint{
    public void importSummary(String summary, String Phone_number, String Password){
        System.out.println("Received from Python:" + summary);
        User this_User = Manager.Login(Phone_number, Password, summary);
        if(this_User != null){
            this_User.setDescription(summary);
        }else{
            Manager.Signup(Phone_number, Password, summary);
            System.out.println("Signup complete");
        }
    }

    public String getSummary(int i){
        return Manager.getUsers().get(i).getDescription();
    }
    private UserManager Manager = new UserManager();

    public UserManager getManager(){
        return Manager;
    }

    public int getTotalNumber(){
        return Manager.users.size();
    }

    public String getPhone_Number(int i){
        return Manager.getUsers().get(i).getPhone_number();
    }

    public static void main(String[] args){
        GatewayServer server = new GatewayServer(new EntryPoint(), 25333);
        server.start();
        System.out.println("Gateway Server Started on port 25333");
    }
}

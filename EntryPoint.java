import py4j.Gateway;
import py4j.GatewayServer;

public class EntryPoint{
    private UserManager Manager = new UserManager();

    public UserManager getManager(){
        return Manager;
    }

    public static void main(String[] args){
        GatewayServer server = new GatewayServer(new EntryPoint());
        server.start();
        System.out.println("Gateway Server Started");
    }
}

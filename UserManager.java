import py4j.*;

import java.util.ArrayList;
import java.util.List;
import java.util.Scanner;

public class UserManager {
    private List<User> users = new ArrayList<>();
    private Scanner scanner = new Scanner(System.in);

    //Register a new user
    public void Signup(String Phone_number, String Password, String Description){
        users.add(new User(Phone_number, Password, Description));
        System.out.println("You successfully logged in");
    }

    public boolean Login(String Phone_number, String Password, String Description){
        for(int i = 0; i < users.size();i++){
            if(users.get(i).getPhone_number().equals(Phone_number)){
                if(users.get(i).getPassword().equals(Password)){
                    return true;
                }else{
                    return false;
                }
            }
        }
        return false;
    }
}

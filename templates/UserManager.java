import py4j.*;

import java.util.ArrayList;
import java.util.List;

public class UserManager {
    public List<User> users = new ArrayList<>();

    //Register a new user
    public User Signup(String Phone_number, String Password, String Description){
        users.add(new User(Phone_number, Password, Description));
        System.out.println("You successfully registered in");
        return users.getLast();
    }

    public User Login(String Phone_number, String Password, String Description){
        for(int i = 0; i < users.size();i++){
            if(users.get(i).getPhone_number().equals(Phone_number)){
                if(users.get(i).getPassword().equals(Password)){
                    return users.get(i);
                }else{
                    return null;
                }
            }
        }
        return null;
    }

    public List<User> getUsers(){
        return users;
    }
}

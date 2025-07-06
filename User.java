public class User {
    private String Phone_number;
    private String Password;
    private String Describtion;
    public User(String Phone_number, String Password, String Describtion){
        this.Phone_number = Phone_number;
        this.Password = Password;
        this.Describtion = Describtion;
    }

    public String getPhone_number(){
        return Phone_number;
    }

    public String getPassword(){
        return Password;
    }

    public String getDescribtion(){
        return Describtion;
    }

    public void setPassword(String Password){
        this.Password = Password;
    }
}

public class User {
    private String Phone_number;
    private String Password;
    private String Description;
    public User(String Phone_number, String Password, String Description){
        this.Phone_number = Phone_number;
        this.Password = Password;
        this.Description = Description;
    }

    public String getPhone_number(){
        return Phone_number;
    }

    public String getPassword(){
        return Password;
    }

    public String getDescription(){
        return Description;
    }

    public void setPassword(String Password){
        this.Password = Password;
    }

    public void setDescription(String Description){
        this.Description = Description;
    }
}

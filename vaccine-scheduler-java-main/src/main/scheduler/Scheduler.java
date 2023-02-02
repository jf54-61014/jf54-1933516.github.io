package scheduler;

import scheduler.db.ConnectionManager;
import scheduler.model.Caregiver;
import scheduler.model.Patient;
import scheduler.model.Vaccine;
import scheduler.util.Util;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.sql.Date;
import java.util.Objects;
import java.util.Random;

public class Scheduler {

    // objects to keep track of the currently logged-in user
    // Note: it is always true that at most one of currentCaregiver and currentPatient is not null
    //       since only one user can be logged-in at a time
    private static Caregiver currentCaregiver = null;
    private static Patient currentPatient = null;

    public static void main(String[] args) throws SQLException {
        // printing greetings text
        System.out.println();
        System.out.println("Welcome to the COVID-19 Vaccine Reservation Scheduling Application!");
        System.out.println("*** Please enter one of the following commands ***");
        System.out.println("> create_patient <username> <password>");  //TODO: implement create_patient (Part 1)
        System.out.println("> create_caregiver <username> <password>");
        System.out.println("> login_patient <username> <password>");  // TODO: implement login_patient (Part 1)
        System.out.println("> login_caregiver <username> <password>");
        System.out.println("> search_caregiver_schedule <date>");  // TODO: implement search_caregiver_schedule (Part 2)
        System.out.println("> reserve <date> <vaccine>");  // TODO: implement reserve (Part 2)
        System.out.println("> upload_availability <date>");
        System.out.println("> cancel <appointment_id>");  // TODO: implement cancel (extra credit)
        System.out.println("> add_doses <vaccine> <number>");
        System.out.println("> show_appointments");  // TODO: implement show_appointments (Part 2)
        System.out.println("> logout");  // TODO: implement logout (Part 2)
        System.out.println("> quit");
        System.out.println();

        // read input from user
        BufferedReader r = new BufferedReader(new InputStreamReader(System.in));
        while (true) {
            System.out.print("> ");
            String response = "";
            try {
                response = r.readLine();
            } catch (IOException e) {
                System.out.println("Please try again!");
            }
            // split the user input by spaces
            String[] tokens = response.split(" ");
            // check if input exists
            if (tokens.length == 0) {
                System.out.println("Please try again!");
                continue;
            }
            // determine which operation to perform
            String operation = tokens[0];
            if (operation.equals("create_patient")) {
                createPatient(tokens);
            } else if (operation.equals("create_caregiver")) {
                createCaregiver(tokens);
            } else if (operation.equals("login_patient")) {
                loginPatient(tokens);
            } else if (operation.equals("login_caregiver")) {
                loginCaregiver(tokens);
            } else if (operation.equals("search_caregiver_schedule")) {
                searchCaregiverSchedule(tokens);
            } else if (operation.equals("reserve")) {
                reserve(tokens);
            } else if (operation.equals("upload_availability")) {
                uploadAvailability(tokens);
            } else if (operation.equals("cancel")) {
                cancel(tokens);
            } else if (operation.equals("add_doses")) {
                addDoses(tokens);
            } else if (operation.equals("show_appointments")) {
                showAppointments(tokens);
            } else if (operation.equals("logout")) {
                logout(tokens);
            } else if (operation.equals("quit")) {
                System.out.println("Bye!");
                return;
            } else {
                System.out.println("Invalid operation name!");
            }
        }
    }

    private static void createPatient(String[] tokens) {
        // TODO: Part 1
       if (tokens.length != 3) {
            System.out.println("Please try again!");
            return;
        }
        String username = tokens[1];
        String password = tokens[2];
        if (usernameExistsPatient(username)) {
            System.out.println("Username taken, try again!");
            return;
        }
        if (usernameExistsPatient(username)) {
            System.out.println("Username taken, try again!");
            return;
        }
        byte[] salt = Util.generateSalt();
        byte[] hash = Util.generateHash(password, salt);
        // create the caregiver
        try {
            currentPatient = new Patient.PatientBuilder(username, salt, hash).build();
            // save to caregiver information to our database
            currentPatient.saveToDB();
            System.out.println(" *** Account created successfully *** ");
        } catch (SQLException e) {
            System.out.println("Create failed");
            e.printStackTrace();
        }
    }

   private static boolean usernameExistsPatient(String username) {
        ConnectionManager cm = new ConnectionManager();
        Connection con = cm.createConnection();

        String selectUsername = "SELECT * FROM Patients WHERE Username = ?";
        try {
            PreparedStatement statement = con.prepareStatement(selectUsername);
            statement.setString(1, username);
            ResultSet resultSet = statement.executeQuery();
            return resultSet.isBeforeFirst();
        } catch (SQLException e) {
            System.out.println("Error occurred when checking username");
            e.printStackTrace();
        } finally {
            cm.closeConnection();
        }
        return true;
    }

    private static void createCaregiver(String[] tokens) {
        // create_caregiver <username> <password>
        // check 1: the length for tokens need to be exactly 3 to include all information (with the operation name)
        if (tokens.length != 3) {
            System.out.println("Please try again!");
            return;
        }
        String username = tokens[1];
        String password = tokens[2];
        // check 2: check if the username has been taken already
        if (usernameExistsCaregiver(username)) {
            System.out.println("Username taken, try again!");
            return;
        }
        byte[] salt = Util.generateSalt();
        byte[] hash = Util.generateHash(password, salt);
        // create the caregiver
        try {
            currentCaregiver = new Caregiver.CaregiverBuilder(username, salt, hash).build();
            // save to caregiver information to our database
            currentCaregiver.saveToDB();
            System.out.println(" *** Account created successfully *** ");
        } catch (SQLException e) {
            System.out.println("Create failed");
            e.printStackTrace();
        }
    }

    private static boolean usernameExistsCaregiver(String username) {
        ConnectionManager cm = new ConnectionManager();
        Connection con = cm.createConnection();

        String selectUsername = "SELECT * FROM Caregivers WHERE Username = ?";
        try {
            PreparedStatement statement = con.prepareStatement(selectUsername);
            statement.setString(1, username);
            ResultSet resultSet = statement.executeQuery();
            // returns false if the cursor is not before the first record or if there are no rows in the ResultSet.
            return resultSet.isBeforeFirst();
        } catch (SQLException e) {
            System.out.println("Error occurred when checking username");
            e.printStackTrace();
        } finally {
            cm.closeConnection();
        }
        return true;
    }

    private static void loginPatient(String[] tokens) {
        // TODO: Part 1
        if (currentCaregiver != null || currentPatient != null) {
            System.out.println("Already logged-in!");
            return;
        }
        if (tokens.length != 3) {
            System.out.println("Please try again!");
            return;
        }
        String username = tokens[1];
        String password = tokens[2];

        Patient patient = null;
        try {
            patient = new Patient.PatientGetter(username, password).get();
        } catch (SQLException e) {
            System.out.println("Error occurred when logging in");
            e.printStackTrace();
        }

        if (patient == null) {
            System.out.println("Please try again!");
        } else {
            System.out.println("Patient logged in as: " + username);
            currentPatient = patient;
        }
    }

    private static void loginCaregiver(String[] tokens) {
        // login_caregiver <username> <password>
        // check 1: if someone's already logged-in, they need to log out first
        if (currentCaregiver != null || currentPatient != null) {
            System.out.println("Already logged-in!");
            return;
        }
        // check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
        if (tokens.length != 3) {
            System.out.println("Please try again!");
            return;
        }
        String username = tokens[1];
        String password = tokens[2];

        Caregiver caregiver = null;
        try {
            caregiver = new Caregiver.CaregiverGetter(username, password).get();
        } catch (SQLException e) {
            System.out.println("Error occurred when logging in");
            e.printStackTrace();
        }
        // check if the login was successful
        if (caregiver == null) {
            System.out.println("Please try again!");
        } else {
            System.out.println("Caregiver logged in as: " + username);
            currentCaregiver = caregiver;
        }
    }

    private static void searchCaregiverSchedule(String[] tokens) throws SQLException {
        // TODO: Part 2
        if (currentCaregiver == null && currentPatient == null) {
            System.out.println("Please login in first!");
            return;
        }
        if (tokens.length != 2) {
            System.out.println("Please try again!");
            return;
        }
        String date = tokens[1];
        Date d = Date.valueOf(date);

        ConnectionManager cm = new ConnectionManager();
        Connection con = cm.createConnection();
        try {
            String searchSchedule = "SELECT Username FROM Availabilities WHERE Time = ?";
            PreparedStatement statement = con.prepareStatement(searchSchedule);
            statement.setDate(1, d);
            ResultSet resultSet = statement.executeQuery();
            System.out.println("Available caregivers for the day:");
            while (resultSet.next()) {
                String name = resultSet.getString("Username");
                System.out.println(name);
            }

            String avail_doses = "SELECT * FROM Vaccines";
            PreparedStatement statement1 = con.prepareStatement(avail_doses);
            ResultSet resultSet1 = statement1.executeQuery();
            System.out.println("Available vaccines:");
            while (resultSet1.next()) {
                String name1 = resultSet1.getString("Name");
                String name2 = resultSet1.getString("Doses");
                System.out.println("name: " + name1 + ",      " + name2 + " doses left");
            }
        } catch (IllegalArgumentException e) {
            System.out.println("Please enter a valid date!");
        } catch (SQLException e) {
            System.out.println("Error occurred when searching schedules");
        } finally {
            cm.closeConnection();
        }
    }

    private static void reserve(String[] tokens) {
        // TODO: Part 2
       if (currentPatient == null) {
            System.out.println("Please login as a patient first!");
            return;
        }
        if (tokens.length != 3) {
            System.out.println("Please try again!");
            return;
        }
        String date = tokens[1];
        String V_name = tokens[2];
        Date d = Date.valueOf(date);
        String p_name = currentPatient.getUsername();

        if (reservationExists(p_name, d)) {
            System.out.println("Already reserved for the day, please try again!");
            return;
        }

        ConnectionManager cm = new ConnectionManager();
        Connection con = cm.createConnection();

        String avail_caregivers = "SELECT Username FROM Availabilities Where Time = ?";
        try {
            PreparedStatement statement = con.prepareStatement(avail_caregivers);
            statement.setDate(1, d);
            ResultSet resultSet = statement.executeQuery();

            String[] tem = new String[1000000];

            int i = 0;
            while (resultSet.next()) {
                String name = resultSet.getString("Username");
                tem[i] = name;
                i++;
            }
            String[] avail_care_name = new String[i];
            for (int j = 0; j < i; j++){
                avail_care_name[j] = tem[j];
            }

            Random rnd = new Random();
            int randomIndex = rnd.nextInt(avail_care_name.length);
            String care_name = avail_care_name[randomIndex-1];

            Random rndint = new Random();
            int App_ID = 10000000 + rndint.nextInt(90000000);
            while(AppIDExists(App_ID)){
                App_ID = 10000000 + rndint.nextInt(90000000);
            }

            currentPatient.saveToApp(App_ID, V_name, d, p_name, care_name);
            currentPatient.deleteAvailability(d, care_name);
            deleteDoses(V_name);
            System.out.println("reservation created! caregiver name: " + care_name + ",  Appointment_ID: " + App_ID);
        } catch (IllegalArgumentException e) {
            System.out.println("Please enter a valid input!");
        } catch (SQLException e) {
            System.out.println("Error occurred when reserving schedule");
        } finally {
            cm.closeConnection();
        }
    }

    private static boolean reservationExists(String username, Date d) {
        ConnectionManager cm = new ConnectionManager();
        Connection con = cm.createConnection();

        String selectUsername = "SELECT * FROM Appointments WHERE Patient_name = ? AND Time = ?";
        try {
            PreparedStatement statement = con.prepareStatement(selectUsername);
            statement.setString(1, username);
            statement.setDate(2, d);
            ResultSet resultSet = statement.executeQuery();
            return resultSet.isBeforeFirst();
        } catch (SQLException e) {
            System.out.println("Error occurred when checking username");
            e.printStackTrace();
        } finally {
            cm.closeConnection();
        }
        return true;
    }

    private static boolean AppIDExists(int App_ID) {
        ConnectionManager cm = new ConnectionManager();
        Connection con = cm.createConnection();

        String selectUsername = "SELECT * FROM Appointments WHERE Appointment_ID = ?";
        try {
            PreparedStatement statement = con.prepareStatement(selectUsername);
            statement.setInt(1, App_ID);
            ResultSet resultSet = statement.executeQuery();
            // returns false if the cursor is not before the first record or if there are no rows in the ResultSet.
            return resultSet.isBeforeFirst();
        } catch (SQLException e) {
            System.out.println("Error occurred when checking username");
            e.printStackTrace();
        } finally {
            cm.closeConnection();
        }
        System.out.println("exist");
        return true;
    }

   private static void deleteDoses(String V_name) {
        Vaccine vaccine = null;
        try {
            vaccine = new Vaccine.VaccineGetter(V_name).get();
        } catch (SQLException e) {
            System.out.println("Error occurred when deleting doses");
            e.printStackTrace();
        }
        // check 3: if getter returns null, it means that we need to create the vaccine and insert it into the Vaccines
        //          table
        if (vaccine == null) {
            System.out.println("vaccine does not exist, please try again!");
        } else {
            // if the vaccine is not null, meaning that the vaccine already exists in our table
            try {
                int num_doses = 1;
                vaccine.decreaseAvailableDoses(num_doses);
            } catch (SQLException e) {
                System.out.println("Error occurred when deleting doses");
                e.printStackTrace();
            }
        }
    }

    private static void uploadAvailability(String[] tokens) {
        // upload_availability <date>
        // check 1: check if the current logged-in user is a caregiver
        if (currentCaregiver == null) {
            System.out.println("Please login as a caregiver first!");
            return;
        }
        // check 2: the length for tokens need to be exactly 2 to include all information (with the operation name)
        if (tokens.length != 2) {
            System.out.println("Please try again!");
            return;
        }
        String date = tokens[1];
        Date d = Date.valueOf(date);
        String c_name = currentCaregiver.getUsername();
        if (uploadAlready(c_name, d)) {
            System.out.println("Already uploaded, try another date!");
            return;
        }

        if (reservedAlready(c_name, d)) {
            System.out.println("Already been reserved for the day, please try again!");
            return;
        }

        try {
            currentCaregiver.uploadAvailability(d);
            System.out.println("Availability uploaded!");
        } catch (IllegalArgumentException e) {
            System.out.println("Please enter a valid date!");
        } catch (SQLException e) {
            System.out.println("Error occurred when uploading availability");
            e.printStackTrace();
        }
    }

    private static boolean uploadAlready(String username, Date d) {
        ConnectionManager cm = new ConnectionManager();
        Connection con = cm.createConnection();

        String selectUsername = "SELECT * FROM Availabilities WHERE Time = ? AND Username = ?";
        try {
            PreparedStatement statement = con.prepareStatement(selectUsername);
            statement.setDate(1, d);
            statement.setString(2, username);
            ResultSet resultSet = statement.executeQuery();
            return resultSet.isBeforeFirst();
        } catch (SQLException e) {
            System.out.println("Error occurred when checking availabilities");
            e.printStackTrace();
        } finally {
            cm.closeConnection();
        }
        return true;
    }

    private static boolean reservedAlready(String username, Date d) {
        ConnectionManager cm = new ConnectionManager();
        Connection con = cm.createConnection();

        String selectUsername = "SELECT * FROM Appointments WHERE Caregiver_name = ? AND Time = ?";
        try {
            PreparedStatement statement = con.prepareStatement(selectUsername);
            statement.setString(1, username);
            statement.setDate(2, d);
            ResultSet resultSet = statement.executeQuery();
            return resultSet.isBeforeFirst();
        } catch (SQLException e) {
            System.out.println("Error occurred when checking username");
            e.printStackTrace();
        } finally {
            cm.closeConnection();
        }
        return true;
    }

    private static void cancel(String[] tokens) {
        // TODO: Extra credit
        if (currentCaregiver == null && currentPatient == null) {
            System.out.println("Please login in first!");
            return;
        }
        if (tokens.length != 2) {
            System.out.println("Please try again!");
            return;
        }

        String ID = tokens[1];
        int App_ID = Integer.valueOf(ID);

        ConnectionManager cm = new ConnectionManager();
        Connection con = cm.createConnection();

        try {
            String App_info = "SELECT * FROM Appointments Where Appointment_ID = ?";
            PreparedStatement statement1 = con.prepareStatement(App_info);
            statement1.setInt(1, App_ID);
            ResultSet resultSet = statement1.executeQuery();
            String time = resultSet.getString("Time");
            String P_name = resultSet.getString("Patient_name");
            String C_name = resultSet.getString("Caregiver_name");

            Date d = Date.valueOf(time);
            if (currentCaregiver != null) {
                String App_name = currentCaregiver.getUsername();
                if (!Objects.equals(App_name, C_name)){
                    System.out.println("Cancellation failed, since it is not caregiver's own appointment");
                    return;
                } else {
                    currentCaregiver.uploadAvailability(d);
                }
            }
            if (currentPatient != null){
                String App_name = currentPatient.getUsername();
                if (!Objects.equals(App_name, P_name)) {
                    System.out.println("Cancellation failed, since it is not patient's own appointment");
                    return;
                } else {
                    currentPatient.uploadAvailability(d, C_name);
                }
            }

            String cancel_appointment = "DELETE FROM Appointments Where Appointment_ID = ?";
            PreparedStatement statement2 = con.prepareStatement(cancel_appointment);
            statement2.setInt(1, App_ID);
            statement2.executeUpdate();
        } catch (IllegalArgumentException e) {
            System.out.println("Please enter a valid input!");
        } catch (SQLException e) {
            System.out.println("Error occurred when canceling schedule");
        } finally {
            cm.closeConnection();
        }
    }

    private static void addDoses(String[] tokens) {
        // add_doses <vaccine> <number>
        // check 1: check if the current logged-in user is a caregiver
        if (currentCaregiver == null) {
            System.out.println("Please login as a caregiver first!");
            return;
        }
        // check 2: the length for tokens need to be exactly 3 to include all information (with the operation name)
        if (tokens.length != 3) {
            System.out.println("Please try again!");
            return;
        }
        String vaccineName = tokens[1];
        int doses = Integer.parseInt(tokens[2]);
        Vaccine vaccine = null;
        try {
            vaccine = new Vaccine.VaccineGetter(vaccineName).get();
        } catch (SQLException e) {
            System.out.println("Error occurred when adding doses");
            e.printStackTrace();
        }
        // check 3: if getter returns null, it means that we need to create the vaccine and insert it into the Vaccines
        //          table
        if (vaccine == null) {
            try {
                vaccine = new Vaccine.VaccineBuilder(vaccineName, doses).build();
                vaccine.saveToDB();
            } catch (SQLException e) {
                System.out.println("Error occurred when adding doses");
                e.printStackTrace();
            }
        } else {
            // if the vaccine is not null, meaning that the vaccine already exists in our table
            try {
                vaccine.increaseAvailableDoses(doses);
            } catch (SQLException e) {
                System.out.println("Error occurred when adding doses");
                e.printStackTrace();
            }
        }
        System.out.println("Doses updated!");
    }

    private static void showAppointments(String[] tokens) {
        // TODO: Part 2
        if (currentCaregiver == null && currentPatient == null) {
            System.out.println("Please login in first!");
            return;
        }
        if (tokens.length != 1) {
            System.out.println("Please try again!");
            return;
        }

        String App_username;
        if (currentCaregiver != null) {
            App_username = currentCaregiver.getUsername();
            ConnectionManager cm = new ConnectionManager();
            Connection con = cm.createConnection();
            String searchSchedule = "SELECT * FROM Appointments WHERE Caregiver_name = ?";
            try {
                PreparedStatement statement = con.prepareStatement(searchSchedule);
                statement.setString(1, App_username);
                ResultSet resultSet = statement.executeQuery();
                while (resultSet.next()) {
                    String App_ID = resultSet.getString("Appointment_ID");
                    String V_name = resultSet.getString("vaccine_name");
                    String time = resultSet.getString("Time");
                    String P_name = resultSet.getString("Patient_name");
                    System.out.println("Appointment_ID: " + App_ID + "," +
                            "Vaccine name: " + V_name + ", " +
                            "Time: "+ time + ", " +
                            "Patient name: " + P_name);
                }
            } catch (IllegalArgumentException e) {
                System.out.println("Please enter a valid date!");
            } catch (SQLException e) {
                System.out.println("Error occurred when searching schedules");
            } finally {
                cm.closeConnection();
            }
        } else {
            App_username = currentPatient.getUsername();
            ConnectionManager cm = new ConnectionManager();
            Connection con = cm.createConnection();
            String searchSchedule = "SELECT * FROM Appointments WHERE Patient_name = ?";
            try {
                PreparedStatement statement = con.prepareStatement(searchSchedule);
                statement.setString(1, App_username);
                ResultSet resultSet = statement.executeQuery();
                while (resultSet.next()) {
                    String App_ID = resultSet.getString("Appointment_ID");
                    String V_name = resultSet.getString("vaccine_name");
                    String time = resultSet.getString("Time");
                    String C_name = resultSet.getString("Caregiver_name");
                    System.out.println("Appointment_ID: " + App_ID + "," +
                            "Vaccine name: " + V_name + ", " +
                            "Time: "+ time + ", " +
                            "Caregiver name: " + C_name);
                }
            } catch (IllegalArgumentException e) {
                System.out.println("Please enter a valid date!");
            } catch (SQLException e) {
                System.out.println("Error occurred when searching schedules");
            } finally {
                cm.closeConnection();
            }
        }
    }

    private static void logout(String[] tokens) {
        // TODO: Part 2
        if (currentCaregiver == null && currentPatient == null) {
            System.out.println("Already logged-out!");
            return;
        }
        if (tokens.length != 1) {
            System.out.println("Please try again!");
            return;
        }

        if (currentCaregiver != null) {
            currentCaregiver = null;
        }
        if (currentPatient != null) {
            currentPatient = null;
        }
        System.out.println("logout successfully!");
    }
}

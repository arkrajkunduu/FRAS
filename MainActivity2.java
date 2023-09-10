package com.example.fras;

import androidx.annotation.NonNull;
import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

import com.google.android.gms.tasks.OnFailureListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.firebase.firestore.DocumentReference;
import com.google.firebase.firestore.DocumentSnapshot;
import com.google.firebase.firestore.FirebaseFirestore;

import java.util.HashMap;
import java.util.Map;

public class MainActivity2 extends AppCompatActivity {

    FirebaseFirestore firestore;
    TextView attendance;
    Button get;
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main2);
        get = findViewById(R.id.get);
        firestore = FirebaseFirestore.getInstance();
        attendance = findViewById(R.id.attendance);
        String username = getIntent().getStringExtra("users");
        get.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                fetchdata(username);
            }
        });

    }
    public void fetchdata(String s){
        DocumentReference document = firestore.collection("users").document(s);
        document.get().addOnSuccessListener(new OnSuccessListener<DocumentSnapshot>() {
                    @Override
                    public void onSuccess(DocumentSnapshot documentSnapshot) {
                        if(documentSnapshot.exists()) {
                            attendance.setText(documentSnapshot.getString("entry"));
                        }
                        else {
                            Toast.makeText(getApplicationContext(),"failed to fetch" ,Toast.LENGTH_SHORT).show();
                        }
                    }
                })
                .addOnFailureListener(new OnFailureListener() {
                    @Override
                    public void onFailure(@NonNull Exception e) {
                        Toast.makeText(getApplicationContext(),"failed to fetch" ,Toast.LENGTH_SHORT).show();
                    }
                });

    }
}
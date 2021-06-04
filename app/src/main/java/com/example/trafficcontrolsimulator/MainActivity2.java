package com.example.trafficcontrolsimulator;

import androidx.appcompat.app.AppCompatActivity;

import android.os.Bundle;

import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.ImageView;
import android.widget.Spinner;
import android.widget.TextView;

import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;

import java.util.Timer;
import java.util.TimerTask;
import java.util.concurrent.TimeUnit;

public class MainActivity2 extends AppCompatActivity {

    Spinner spinner1;
    Spinner spinner2;

    DatabaseReference reff;
    Button requestb;
    String light;
    String trafficlight;
    ImageView road;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main2);

        spinner1 = findViewById(R.id.spinner1);
        spinner2 = findViewById(R.id.spinner2);

        ArrayAdapter adapter1 = ArrayAdapter.createFromResource(this, R.array.Controller, android.R.layout.simple_spinner_item);
        spinner1.setAdapter(adapter1);

        ArrayAdapter adapter2 = ArrayAdapter.createFromResource(this, R.array.Lights, android.R.layout.simple_spinner_item);
        spinner2.setAdapter(adapter2);

        TextView carros1 = findViewById(R.id.textView6);
        TextView carros2 = findViewById(R.id.textView2);

        requestb = findViewById(R.id.button);
        reff = FirebaseDatabase.getInstance().getReference();
        requestb.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                trafficlight = spinner1.getSelectedItem().toString();
                light = spinner2.getSelectedItem().toString();

                reff.child("Request").child("Traffic Light").setValue(trafficlight);
                reff.child("Request").child("Light").setValue(light);

            }
        });

        road = findViewById(R.id.imageView2);
        DatabaseReference reffread = reff.child("crossing");
        reffread.addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(DataSnapshot snapshot) {
                String cars1 = snapshot.child("street1_cars").getValue().toString();
                String cars2 = snapshot.child("street2_cars").getValue().toString();
                String street1 = snapshot.child("street1").getValue().toString();
                String street2 = snapshot.child("street2").getValue().toString();
                String pedestrian1 = snapshot.child("street1_pedestrians").getValue().toString();
                //String pedestrian2= snapshot.child("street2_pedestrians").getValue().toString();

                carros1.setText(cars1);
                carros2.setText(cars2);

                //Acrescentar timers e imagens yellow
                //ImageView road = findViewById(R.id.imageView2);

                if (street1.equals("Green") && street2.equals("Red") && pedestrian1.equals("Red")) {

                    road.setImageResource(R.drawable.estado4);

                    Timer myTimer = new Timer();
                    TimerTask t = new TimerTask() {
                        @Override
                        public void run() {
                            runOnUiThread(new Runnable() {

                                @Override
                                public void run() {
                                    road.setImageResource(R.drawable.estado1);
                                }
                            });
                        }
                    };

                    myTimer.schedule(t, 1000);

                } else if (street1.equals("Red") && street2.equals("Green") && pedestrian1.equals("Green")) {

                    road.setImageResource(R.drawable.estado2);

                    Timer myTimer = new Timer();
                    TimerTask t = new TimerTask() {
                        @Override
                        public void run() {
                            runOnUiThread(new Runnable() {

                                @Override
                                public void run() {
                                    road.setImageResource(R.drawable.estado3);

                                }
                            });

                        }
                    };

                    myTimer.schedule(t, 1000);

                }

            }

            @Override
            public void onCancelled(DatabaseError error) {

            }
        });

    }

}
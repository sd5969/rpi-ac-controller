package com.sdlynx.rpiaccontroller;

import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.os.AsyncTask;
import android.view.View;
import android.view.View.OnClickListener;
import java.net.URL;
import java.net.HttpURLConnection;
import java.io.DataOutputStream;
import java.nio.charset.Charset;

public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        findViewById(R.id.ac_power).setOnClickListener(new OnClickListener()
        {
            public void onClick(View v)
            {
                System.out.println("Clicked AC Power");
                new LongRunningGetIO().execute("power-switch", "remote");
                new LongRunningGetIO().execute("power-switch", "local");
            }
        });

        findViewById(R.id.temp_up).setOnClickListener(new OnClickListener()
        {
            public void onClick(View v)
            {
                System.out.println("Clicked Temp Up");
                new LongRunningGetIO().execute("increase-temperature", "remote");
                new LongRunningGetIO().execute("increase-temperature", "local");
            }
        });

        findViewById(R.id.temp_down).setOnClickListener(new OnClickListener()
        {
            public void onClick(View v)
            {
                System.out.println("Clicked Temp Down");
                new LongRunningGetIO().execute("decrease-temperature", "remote");
                new LongRunningGetIO().execute("decrease-temperature", "local");
            }
        });

        findViewById(R.id.hdmi_1).setOnClickListener(new OnClickListener()
        {
            public void onClick(View v)
            {
                System.out.println("Clicked HDMI 1");
                new LongRunningGetIO().execute("hdmi-one", "remote");
                new LongRunningGetIO().execute("hdmi-one", "local");
            }
        });

        findViewById(R.id.hdmi_2).setOnClickListener(new OnClickListener()
        {
            public void onClick(View v)
            {
                System.out.println("Clicked HDMI 2");
                new LongRunningGetIO().execute("hdmi-two", "remote");
                new LongRunningGetIO().execute("hdmi-two", "local");
            }
        });

        findViewById(R.id.hdmi_3).setOnClickListener(new OnClickListener()
        {
            public void onClick(View v)
            {
                System.out.println("Clicked HDMI 3");
                new LongRunningGetIO().execute("hdmi-three", "remote");
                new LongRunningGetIO().execute("hdmi-three", "local");
            }
        });
    }

    private class LongRunningGetIO extends AsyncTask<String, Void, String> {

        private Exception exception;
        static final String POST_DATA = "{}";
        final String[] API_BASE_URLS = new String[] {"http://nyc.sanjitdutta.com:8181/api/", "http://192.168.1.123:8181/api/"};
        final byte[] POST_DATA_BYTES = POST_DATA.getBytes(Charset.forName("UTF-8"));
        final int POST_DATA_LENGTH = POST_DATA_BYTES.length;

        protected void onPreExecute() {}

        protected String doInBackground(String... args) {
            final int apiIndex = args[1] == "local" ? 1 : 0;
            try {
                URL url = new URL(API_BASE_URLS[apiIndex] + args[0]);
                System.out.println("Hitting endpoint: " + url);

                HttpURLConnection urlConnection = (HttpURLConnection) url.openConnection();
                urlConnection.setDoOutput(true);
                urlConnection.setInstanceFollowRedirects(false);
                urlConnection.setRequestMethod("POST");
                urlConnection.setRequestProperty("Content-Type", "application/json");
                urlConnection.setRequestProperty("charset", "utf-8");
                urlConnection.setRequestProperty("Content-Length", Integer.toString(POST_DATA_LENGTH));
                urlConnection.setUseCaches(false);

                DataOutputStream wr = new DataOutputStream(urlConnection.getOutputStream());
                wr.write(POST_DATA_BYTES);
                wr.flush();
                wr.close();

                System.out.println("Response code: " + urlConnection.getResponseCode());
            }
            catch(Exception e) {
                System.out.println("ERROR: " + e.toString());
                return null;
            }
            return "";
        }

        protected void onPostExecute(String response) {}
    }
}

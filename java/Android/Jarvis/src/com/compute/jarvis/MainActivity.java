package com.compute.jarvis;

import android.app.Activity;
import android.app.ActionBar;
import android.app.Fragment;
import android.os.Bundle;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.RadioButton;
import android.widget.TextView;
import android.os.Build;

public class MainActivity extends Activity {

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		Log.i("Lifecycle", "onCreate called");
		if (savedInstanceState == null) {
			getFragmentManager().beginTransaction()
					.add(R.id.container, new PlaceholderFragment()).commit();
		}
	}
	protected void onStart(){
		super.onStart();
		Log.i("LifeCycle", "onStart called");
	}
	
	protected void onResume(){
		super.onResume();
		Log.i("Lifecycle", "onResume called");
	}
	
	protected void onStop(){
		super.onStop();
		Log.i("Lifecycle", "onStop called");
	}
	
	protected void onPause(){
		super.onPause();
		Log.i("Lifecycle", "onPause called");
	}
	
	protected void onDestroy(){
		super.onDestroy();
		Log.i("Lifecycle", "onDestroy called");
	}

	@Override
	public boolean onCreateOptionsMenu(Menu menu) {

		// Inflate the menu; this adds items to the action bar if it is present.
		getMenuInflater().inflate(R.menu.main, menu);
		return true;
	}

	@Override
	public boolean onOptionsItemSelected(MenuItem item) {
		// Handle action bar item clicks here. The action bar will
		// automatically handle clicks on the Home/Up button, so long
		// as you specify a parent activity in AndroidManifest.xml.
		int id = item.getItemId();
		if (id == R.id.action_settings) {
			return true;
		}
		return super.onOptionsItemSelected(item);
	}

	/**
	 * A placeholder fragment containing a simple view.
	 */
	public static class PlaceholderFragment extends Fragment {

		public PlaceholderFragment() {
		}

		@Override
		public View onCreateView(LayoutInflater inflater, ViewGroup container,
				Bundle savedInstanceState) {
			View rootView = inflater.inflate(R.layout.fragment_main, container,
					false);
			return rootView;
		}
	}
	public void onButtonTouch(View v) {
		TextView tv = (TextView) findViewById(R.id.textView1);
		tv.setText("Hello, World!");
	}
	
	public void btnClicked(View v){
		RadioButton radio = (RadioButton) findViewById(R.id.radioButton1);
		if (radio.isChecked()) radio.setChecked(false);
		else radio.setChecked(true);
	}
	
	

}

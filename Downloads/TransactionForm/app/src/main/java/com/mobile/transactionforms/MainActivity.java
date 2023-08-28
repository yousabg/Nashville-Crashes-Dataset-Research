package com.mobile.transactionforms;

import androidx.appcompat.app.AppCompatActivity;

import android.content.ContentValues;
import android.content.Intent;
import android.database.Cursor;
import android.graphics.Color;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.SurfaceControl;
import android.view.View;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.EditText;
import android.widget.RadioButton;
import android.widget.RadioGroup;
import android.widget.Spinner;
import android.widget.TextView;
import android.widget.Toast;

import java.text.DecimalFormat;

public class MainActivity extends AppCompatActivity {

    Spinner orderType;
    EditText ticker;
    EditText companyName;
    RadioButton buy;
    RadioButton sell;
    RadioGroup transType;
    EditText ppShare;
    EditText confirmCode;
    TextView tickerText;
    TextView companyNameText;
    EditText transAmount;
    TextView transAmountText;
    TextView ppShareText;
    TextView confirmCodeText;
    String selectedSpinner;

    private static final DecimalFormat df = new DecimalFormat("0.00");

    TextWatcher transWatcher = new TextWatcher() {
        String afterDec = "";

        @Override
        public void beforeTextChanged(CharSequence s, int start, int count, int after) {


        }

        @Override
        public void onTextChanged(CharSequence s, int start, int before, int count) {
            if (transAmount.getText().toString().contains(".")) {
                afterDec = transAmount.getText().toString().substring(transAmount.getText().toString().indexOf(".") +1);
            }
            if (afterDec.length() > 2) {
                afterDec = transAmount.getText().toString().substring(0 ,transAmount.getText().toString().indexOf(".") + 3);
                transAmount.setText(afterDec);
                transAmount.setSelection(transAmount.length());
            }
        }

        @Override
        public void afterTextChanged(Editable editable) {

        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.table_layout);

        setSpinner();
        orderType.setSelection(2);
        orderType.setOnItemSelectedListener(spinnerListener);

        ticker = findViewById(R.id.ticker);
        companyName = findViewById(R.id.companyName);
        buy = findViewById(R.id.Buy);
        sell = findViewById(R.id.Sell);
        transType = findViewById(R.id.transType);
        transAmount = findViewById(R.id.transactionAmount);
        transAmount.addTextChangedListener(transWatcher);
        ppShare = findViewById(R.id.pricePerShare);
        ppShare.addTextChangedListener(ppShareWatcher);
        orderType = findViewById(R.id.orderType);
        confirmCode = findViewById(R.id.confirmCode);
        tickerText = findViewById(R.id.tickerText);
        companyNameText = findViewById(R.id.companyNameText);
        transAmountText = findViewById(R.id.transactionAmountText);
        ppShareText = findViewById(R.id.ppshareText);
        confirmCodeText = findViewById(R.id.confirmationCodeText);


    }

    public void reset(View view) {
        ticker.setText("DIS");
        companyName.setText("Disney");
        buy.setChecked(true);
        transAmount.setText("0.00");
        ppShare.setText("0.00");
        confirmCode.setText("");
    }

    public String newText = "";
    public boolean editing = false;
    private static final int MAX_LENGTH = 4;
    private static final int MIN_LENGTH = 8;


    //String transPrevious = transAmount.toString();


    TextWatcher ppShareWatcher = new TextWatcher() {
        String afterDec = "";
        @Override
        public void beforeTextChanged(CharSequence s, int start, int count, int after) {

        }

        @Override
        public void onTextChanged(CharSequence s, int start, int before, int count) {
            if (ppShare.getText().toString().contains(".")) {
                afterDec = ppShare.getText().toString().substring(ppShare.getText().toString().indexOf(".") +1);
            }
            if (afterDec.length() > 2) {
                afterDec = ppShare.getText().toString().substring(0 ,ppShare.getText().toString().indexOf(".") + 3);
                ppShare.setText(afterDec);
                ppShare.setSelection(ppShare.length());
            }
        }

        @Override
        public void afterTextChanged(Editable editable) {

        }


    };

    private AdapterView.OnItemSelectedListener spinnerListener = new AdapterView.OnItemSelectedListener() {
        @Override
        public void onItemSelected(AdapterView<?> parent, View view, int position, long id) {
            //Toast.makeText(getApplicationContext(),((TextView) view).getText(),
            //        Toast.LENGTH_SHORT).show();
            selectedSpinner = parent.getItemAtPosition(position).toString();
        }

        @Override
        public void onNothingSelected(AdapterView<?> parent) {
            Toast.makeText(getApplicationContext(),"You didn't select anything" ,Toast.LENGTH_SHORT).show();
        }
    };

    private void setSpinner() {
        orderType = findViewById(R.id.orderType);

                String[] roles = new String[]{ "Market", "Limit", "Stop" };
                ArrayAdapter<String> adapter2 =
                        new ArrayAdapter<String>(this,
                                android.R.layout.simple_spinner_item, roles);
                adapter2.setDropDownViewResource(android.R.layout.simple_spinner_dropdown_item);
                orderType.setAdapter(adapter2);
    }

    public void submitClicked(View view) {
        tickerText.setTextColor(Color.BLACK);
        companyNameText.setTextColor(Color.BLACK);
        transAmountText.setTextColor(Color.BLACK);
        ppShareText.setTextColor(Color.BLACK);
        confirmCodeText.setTextColor(Color.BLACK);
        confirmCodeText.setTextColor(Color.BLACK);

        String[] confirmations = getResources().getStringArray(R.array.confirmations);
        boolean alphaChars = false;
        boolean wrongCode = false;
//        int confirmCount = 0;
        for (int i = 0; i < companyName.getText().toString().length(); i ++) {
            if (!Character.isLetterOrDigit(companyName.getText().toString().charAt(i))) {
                alphaChars = true;
            }
//        }
//        for (String confirmation: confirmations) {
//            if (!confirmCode.getText().toString().equals(confirmation)) {
//                confirmCount++;
//            }
        }
        Cursor tempCursor = getContentResolver().query(TransactionProvider.CONTENT_URI, null, null, null, null);
        while (tempCursor.moveToNext()) {
            if (confirmCode.getText().toString().equals(tempCursor.getString(1))) {
                wrongCode = true;
            }
        }

        if (ticker.getText().toString().equals("") || companyName.getText().toString().equals("") || transAmount.getText().toString().equals("") || ppShare.getText().toString().equals("") || confirmCode.getText().toString().equals("")) {
            if (ticker.getText().toString().equals("")) {
            tickerText.setTextColor(Color.RED);
            } else if (companyName.getText().toString().equals("")) {
                companyNameText.setTextColor(Color.RED);
            } else if (transAmount.getText().toString().equals("")) {
                transAmountText.setTextColor(Color.RED);
            } else if (ppShare.getText().toString().equals("")) {
                ppShareText.setTextColor(Color.RED);
            } else if (confirmCode.getText().toString().equals("")) {
                confirmCodeText.setTextColor(Color.RED);
            }
            Toast.makeText(this, "One or more of the boxes is empty.",Toast.LENGTH_SHORT).show();
        } else if (ticker.getText().toString().length() < 3 || ticker.getText().toString().length() > 6) {
            tickerText.setTextColor(Color.RED);
            Toast.makeText(this, "Ticker length must be between 3 and 6 characters.",Toast.LENGTH_SHORT).show();
        } else if (ticker.getText().toString().charAt(0) != companyName.getText().toString().charAt(0)) {
            tickerText.setTextColor(Color.RED);
            companyNameText.setTextColor(Color.RED);
            Toast.makeText(this, "First letter of the ticker and the company name must be the same.",Toast.LENGTH_SHORT).show();
        } else if (companyName.getText().toString().length() < 6 || companyName.getText().toString().length() > 20) {
            companyNameText.setTextColor(Color.RED);
            Toast.makeText(this, "Company name must be between 6 and 20 characters.",Toast.LENGTH_SHORT).show();
        } else if (alphaChars) {
            confirmCodeText.setTextColor(Color.RED);
            Toast.makeText(this, "Confirmation code may not contain any non-alphanumeric characters.",Toast.LENGTH_SHORT).show();
        } else if (confirmCode.getText().toString().length() < 4 || confirmCode.getText().toString().length() > 8) {
            confirmCodeText.setTextColor(Color.RED);
            Toast.makeText(this, "Confirmation code must be between 4 and 8 characters.",Toast.LENGTH_SHORT).show();
        } else if (wrongCode) {
            confirmCodeText.setTextColor(Color.RED);
            Toast.makeText(this, "Confirmation code has been used previously.",Toast.LENGTH_SHORT).show();
        } else {
            ContentValues mNewValues = new ContentValues();

            mNewValues.put(TransactionProvider.COLUMN_TICKER, ticker.getText().toString().trim());
            mNewValues.put(TransactionProvider.COLUMN_COMPANYNAME, companyName.getText().toString().trim());
            if (buy.isChecked()) {
                mNewValues.put(TransactionProvider.COLUMN_TRANSACTIONTYPE, "Buy");
            } else {
                mNewValues.put(TransactionProvider.COLUMN_TRANSACTIONTYPE, "Sell");
            }
            mNewValues.put(TransactionProvider.COLUMN_TRANSACTIONAMOUNT, transAmount.getText().toString().trim());
            mNewValues.put(TransactionProvider.COLUMN_PRICEPERSHARE, ppShare.getText().toString().trim());
            mNewValues.put(TransactionProvider.COLUMN_TYPEOFORDER, selectedSpinner);
            mNewValues.put(TransactionProvider.COLUMN_CONFIRMATIONCODE, confirmCode.getText().toString());


            getContentResolver().insert(TransactionProvider.CONTENT_URI, mNewValues);
            Toast.makeText(this, "SUCCESS: INFORMATION STORED IN DATABASE",Toast.LENGTH_LONG).show();
            Intent intent = new Intent(getApplicationContext(), TransactionContent.class);
            startActivity(intent);
        }
    }
}

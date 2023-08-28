package com.mobile.transactionforms;

import androidx.appcompat.app.AppCompatActivity;

import android.app.ListActivity;
import android.content.Context;
import android.database.Cursor;
import android.os.Bundle;
import android.util.Log;
import android.view.ContextMenu;
import android.view.LayoutInflater;
import android.view.MenuInflater;
import android.view.MenuItem;
import android.view.View;
import android.view.ViewGroup;
import android.widget.AdapterView;
import android.widget.ArrayAdapter;
import android.widget.BaseAdapter;
import android.widget.CursorAdapter;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import java.util.zip.Inflater;

public class TransactionContent extends AppCompatActivity {

    ListView listview;
    Cursor mCursor;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_transaction_content);

        listview = findViewById(R.id.transactionList);
        mCursor = getContentResolver().query(TransactionProvider.CONTENT_URI, null, null, null, null);
        CursorAdapter cursorAdapter = new CursorAdapter(this, mCursor) {
            @Override
            public View newView(Context context, Cursor cursor, ViewGroup viewGroup) {
                View rootView = LayoutInflater.from(context).inflate(R.layout.custom_list_layout,viewGroup,false);
                return rootView;
            }

            @Override
            public void bindView(View view, Context context, Cursor cursor) {
                TextView labels = view.findViewById(R.id.Labels);
                TextView ordnum = view.findViewById(R.id.OrderNumC);
                TextView ticker = view.findViewById(R.id.TickerC);
                TextView compName = view.findViewById(R.id.compNameC);
                TextView transType = view.findViewById(R.id.transTypeC);
                TextView transAmount = view.findViewById(R.id.transAmountC);
                TextView ppshare = view.findViewById(R.id.pricePerShareC);
                TextView orderType = view.findViewById(R.id.OrderTypeC);
                TextView confirmCode = view.findViewById(R.id.confirmCode);
                //0 is ID
                //1 is confirm code
                //2 is ticker
                //3 is company name
                //4 is transaction type
                //5 is transaction amount
                //6 is price per sahre
                //7 is order type
                String l = "Order Number:\n"+
                        "Ticker:\n"+
                        "Company Name:\n"+
                        "Transaction Type:\n"+
                        "Transaction Amount:\n" +
                        "Price Per Share:\n" +
                        "Order Type:";
                ordnum.setText(cursor.getString(0));
                ticker.setText(cursor.getString(2));
                compName.setText(cursor.getString(3));
                transType.setText(cursor.getString(4));
                transAmount.setText(cursor.getString(5));
                ppshare.setText(cursor.getString(6));
                orderType.setText(cursor.getString(7));

                labels.setText(l);
            }
        };
        listview.setAdapter(cursorAdapter);

        registerForContextMenu(listview);
    }

    @Override
    public void onCreateContextMenu(ContextMenu menu, View v, ContextMenu.ContextMenuInfo menuInfo) {
        super.onCreateContextMenu(menu, v, menuInfo);
        MenuInflater inflater = getMenuInflater();
        inflater.inflate(R.menu.transaction_menu, menu);
    }

    @Override
    public boolean onContextItemSelected(MenuItem item) {
        AdapterView.AdapterContextMenuInfo info = (AdapterView.AdapterContextMenuInfo) item.getMenuInfo();
        int position = info.position;
        if (item.getItemId() == R.id.delete_option) {
            String mSelectionClause = " _id = ? ";


            TextView orderNum = info.targetView.findViewById(R.id.OrderNumC);


            String[] mSelectionArgs = {orderNum.getText().toString()};

           int a = getContentResolver().delete(TransactionProvider.CONTENT_URI, mSelectionClause,
                    mSelectionArgs);

            mCursor = getContentResolver().query(TransactionProvider.CONTENT_URI, null, null, null, null);
            CursorAdapter cursorAdapter = new CursorAdapter(this, mCursor) {
                @Override
                public View newView(Context context, Cursor cursor, ViewGroup viewGroup) {
                    View rootView = LayoutInflater.from(context).inflate(R.layout.custom_list_layout,viewGroup,false);
                    return rootView;
                }

                @Override
                public void bindView(View view, Context context, Cursor cursor) {
                    TextView labels = view.findViewById(R.id.Labels);
                    TextView ordnum = view.findViewById(R.id.OrderNumC);
                    TextView ticker = view.findViewById(R.id.TickerC);
                    TextView compName = view.findViewById(R.id.compNameC);
                    TextView transType = view.findViewById(R.id.transTypeC);
                    TextView transAmount = view.findViewById(R.id.transAmountC);
                    TextView ppshare = view.findViewById(R.id.pricePerShareC);
                    TextView orderType = view.findViewById(R.id.OrderTypeC);
                    TextView confirmCode = view.findViewById(R.id.confirmCode);
                    //0 is ID
                    //1 is confirm code
                    //2 is ticker
                    //3 is company name
                    //4 is transaction type
                    //5 is transaction amount
                    //6 is price per sahre
                    //7 is order type
                    String l = "Order Number:\n"+
                            "Ticker:\n"+
                            "Company Name:\n"+
                            "Transaction Type:\n"+
                            "Transaction Amount:\n" +
                            "Price Per Share:\n" +
                            "Order Type:";
                    ordnum.setText(cursor.getString(0));
                    ticker.setText(cursor.getString(2));
                    compName.setText(cursor.getString(3));
                    transType.setText(cursor.getString(4));
                    transAmount.setText(cursor.getString(5));
                    ppshare.setText(cursor.getString(6));
                    orderType.setText(cursor.getString(7));

                    labels.setText(l);
                }
            };
            listview.setAdapter(cursorAdapter);
            ((BaseAdapter) listview.getAdapter()).notifyDataSetChanged();

        }

        return true;
    }
}
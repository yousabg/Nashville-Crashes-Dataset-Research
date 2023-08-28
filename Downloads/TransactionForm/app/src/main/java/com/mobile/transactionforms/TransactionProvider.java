package com.mobile.transactionforms;

import android.content.ContentProvider;
import android.content.ContentValues;
import android.content.Context;
import android.content.UriMatcher;
import android.database.Cursor;
import android.database.sqlite.SQLiteDatabase;
import android.database.sqlite.SQLiteOpenHelper;
import android.net.Uri;


public class TransactionProvider extends ContentProvider {

    public final static String DBNAME = "NameDatabase";

    protected static final class MainDatabaseHelper extends SQLiteOpenHelper {
        MainDatabaseHelper(Context context) {
            super(context, DBNAME, null, 1);
        }
        @Override
        public void onCreate(SQLiteDatabase db) {
            db.execSQL(SQL_CREATE_MAIN);
        }
        @Override
        public void onUpgrade(SQLiteDatabase arg0, int arg1, int arg2) {
        }
    };

    public final static String TABLE_TRANSACTIONTABLE = "transac";
    public final static String COLUMN_TICKER = "ticker";
    public final static String COLUMN_COMPANYNAME = "companyname";
    public final static String COLUMN_TRANSACTIONTYPE = "transactiontype";
    public final static String COLUMN_TRANSACTIONAMOUNT = "transactionamount";
    public final static String COLUMN_PRICEPERSHARE = "pricepershare";
    public final static String COLUMN_TYPEOFORDER = "typeoforder";
    public final static String COLUMN_CONFIRMATIONCODE = "confirmationcode";


    public static final String AUTHORITY = "com.mobile.transactionforms.provider";
    public static final Uri CONTENT_URI = Uri.parse(
            "content://" + AUTHORITY +"/" + TABLE_TRANSACTIONTABLE);

    private static UriMatcher sUriMatcher;

    private MainDatabaseHelper dbHelper;

    private static final String SQL_CREATE_MAIN = "CREATE TABLE " +
            TABLE_TRANSACTIONTABLE +  // Table's name
            "(" +
            " _id INTEGER PRIMARY KEY, " +
            COLUMN_CONFIRMATIONCODE +
            " TEXT, " +
            COLUMN_TICKER +
            " TEXT," +
            COLUMN_COMPANYNAME+
            " TEXT," +
            COLUMN_TRANSACTIONTYPE +
            " TEXT," +
            COLUMN_TRANSACTIONAMOUNT +
            " INTEGER," +
            COLUMN_PRICEPERSHARE +
            " INTEGER," +
            COLUMN_TYPEOFORDER +
            " TEXT)";




    public TransactionProvider() {
    }

    @Override
    public int delete(Uri uri, String selection, String[] selectionArgs) {
        return dbHelper.getWritableDatabase().delete(TABLE_TRANSACTIONTABLE, selection, selectionArgs);
    }

    @Override
    public String getType(Uri uri) {
        // TODO: Implement this to handle requests for the MIME type of the data
        // at the given URI.
        throw new UnsupportedOperationException("Not yet implemented");
    }

    @Override
    public Uri insert(Uri uri, ContentValues values) {
        String ticker = values.getAsString(COLUMN_TICKER).trim();
        String cname = values.getAsString(COLUMN_COMPANYNAME).trim();
        String transtype = values.getAsString(COLUMN_TRANSACTIONTYPE).trim();
        String transamount = values.getAsString(COLUMN_TRANSACTIONAMOUNT).trim();
        String ppshare = values.getAsString(COLUMN_PRICEPERSHARE).trim();
        String ordertype = values.getAsString(COLUMN_TYPEOFORDER).trim();
        //String confirmcode = values.getAsString(COLUMN_CONFIRMATIONCODE).trim();

        if (ticker.equals(""))
            return null;

        if (cname.equals(""))
            return null;

        if (transtype.equals(""))
            return null;

        if (transamount.equals(""))
            return null;

        if (ppshare.equals(""))
            return null;

        if (ordertype.equals(""))
            return null;

        //if (confirmcode.equals(""))
        //    return null;

        long id = dbHelper.getWritableDatabase().insert(TABLE_TRANSACTIONTABLE, null, values);

        return Uri.withAppendedPath(CONTENT_URI, "" + id);

    }

    @Override
    public boolean onCreate() {
        dbHelper = new MainDatabaseHelper(getContext());
        return true;
    }

    @Override
    public Cursor query(Uri uri, String[] projection, String selection,
                        String[] selectionArgs, String sortOrder) {
        return dbHelper.getReadableDatabase().query(TABLE_TRANSACTIONTABLE, projection, selection, selectionArgs,
                null, null, sortOrder);
    }

    @Override
    public int update(Uri uri, ContentValues values, String selection,
                      String[] selectionArgs) {
        return dbHelper.getWritableDatabase().update(TABLE_TRANSACTIONTABLE, values, selection, selectionArgs);
    }
}
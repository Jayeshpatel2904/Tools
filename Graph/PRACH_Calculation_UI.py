import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox
from geopy.distance import geodesic

def select_file():
    """Opens file dialog to select an Excel file."""
    file_path = filedialog.askopenfilename(title="Select Excel File", filetypes=[("Excel Files", "*.xlsx *.xls")])
    if file_path:
        file_entry.delete(0, tk.END)
        file_entry.insert(0, file_path)

def process_file():
    """Processes the selected Excel file and saves output."""
    file_path = file_entry.get()
    
    if not file_path:
        messagebox.showerror("Error", "Please select an Excel file first.")
        return

    vendor = vendor_var.get()
    task = task_var.get()  # Get selected vendor

    try:
        # Load Excel sheets
        df_sites = pd.read_excel(file_path, sheet_name="Sites")
        df_nrs = pd.read_excel(file_path, sheet_name="NR_Sector_Carriers")

        # Strip spaces from column names
        df_sites.columns = df_sites.columns.str.strip()
        df_nrs.columns = df_nrs.columns.str.strip()

        # If Samsung, keep only the first row per Site ID
        if vendor == "Samsung" and task == "First Zadoff Chu Sequence":
            df_nrs = df_nrs[df_nrs["Sector ID"] == "n66_AWS-4_DL_1"]

        elif vendor == "Mavenir" or task == "Physical Cell ID":
            df_nrs = df_nrs[df_nrs["Sector ID"].str.contains("n66_AWS-4_DL", na=False)]

        # Merge Latitude and Longitude from Sites into NR_Sector_Carriers
        df_merged = df_nrs.merge(df_sites[['Site ID', 'Latitude', 'Longitude']], on='Site ID', how='left')


        columns_to_keep = ["Site ID", "Sector ID", "Physical Cell ID", "First Zadoff Chu Sequence", "Latitude", "Longitude"]
        df_merged = df_merged[columns_to_keep]

        print(df_merged)

        # Function to find the closest site with the same "First Zadoff Chu Sequence"
        def find_closest_site(row, df_merged):
            same_zadoff = df_merged[df_merged[task] == row[task]]
            if same_zadoff.empty:
                return None, None
            
            current_location = (row['Latitude'], row['Longitude'])
            min_distance = float('inf')
            closest_site_id = None
            
            for _, site in same_zadoff.iterrows():
                site_location = (site['Latitude'], site['Longitude'])
                distance = geodesic(current_location, site_location).km
                if distance > 0 and distance < min_distance:
                    min_distance = distance
                    closest_site_id = site['Site ID']
            
            mile_distance = min_distance * 0.621371

            return closest_site_id, min_distance, mile_distance

        # Apply function to find closest site
        df_merged[['Closest Site ID', 'Distance(km)', 'Distance(mile)']] = df_merged.apply(lambda row: pd.Series(find_closest_site(row, df_merged)), axis=1)


        # Ask user for save location
        save_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                 filetypes=[("Excel Files", "*.xlsx")],
                                                 title="Save Processed File")
        if save_path:
            df_merged.to_excel(save_path, index=False)
            messagebox.showinfo("Success", f"Updated file saved as:\n{save_path}")
        else:
            messagebox.showwarning("Cancelled", "Save operation cancelled.")
    
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

# Create UI window
root = tk.Tk()
root.title("PRACH and PCI Intersite Distance Calculator")
root.geometry("500x200")
root.resizable(False, False)  # **Fix window size**

# File selection field
tk.Label(root, text="Select Excel File:").grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="w")
file_entry = tk.Entry(root, width=50)
file_entry.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="w")
tk.Button(root, text="Browse", command=select_file).grid(row=1, column=2, padx=10, pady=5)

# **Organizing Task & Vendor Selection**
frame = tk.Frame(root)
frame.grid(row=2, column=0, columnspan=2, padx=10, pady=5, sticky="w")

# **Task Selection (Left)**
task_var = tk.StringVar(value="First Zadoff Chu Sequence")  # Default task
tk.Label(frame, text="Select TASK:").grid(row=0, column=0, sticky="w", padx=5)
tk.Radiobutton(frame, text="First Zadoff Chu Sequence", variable=task_var, value="First Zadoff Chu Sequence").grid(row=1, column=0, sticky="w", padx=5)
tk.Radiobutton(frame, text="Physical Cell ID", variable=task_var, value="Physical Cell ID").grid(row=2, column=0, sticky="w", padx=5)

# **Vendor Selection (Right)**
vendor_var = tk.StringVar(value="Mavenir")  # Default vendor
tk.Label(frame, text="Select Vendor:").grid(row=0, column=1, sticky="e", padx=50)
tk.Radiobutton(frame, text="Mavenir", variable=vendor_var, value="Mavenir").grid(row=1, column=1, sticky="e", padx=50)
tk.Radiobutton(frame, text="Samsung", variable=vendor_var, value="Samsung").grid(row=2, column=1, sticky="e", padx=50)

# Run button
tk.Button(root, text="Run", command=process_file, bg="green", fg="white", font=("Arial", 10, "bold")).grid(row=3, column=0, columnspan=3, pady=10)




# Start UI loop
root.mainloop()



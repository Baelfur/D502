import sqlite3
import pandas as pd
import os

DB_FILE = "synth/sqlite/d502_assets.db"

def load_table(conn, table_name):
    return pd.read_sql_query(f"SELECT * FROM {table_name}", conn)

def create_lightspeed_asset(df_obs, df_inv, df_ipam):
    # Join observability and inventory on IP and hostname
    obs_inv = pd.merge(
        df_obs,
        df_inv,
        left_on=["obs_ip_address", "obs_hostname"],
        right_on=["inv_ip_address", "inv_hostname"],
        how="left"
    )

    # Join with IPAM on IP address
    full = pd.merge(
        obs_inv,
        df_ipam,
        left_on="obs_ip_address",
        right_on="ipam_ip_address",
        how="left"
    )

    # Compute missing flags
    missing_in_inventory = full["inv_asset_id"].isna()
    missing_in_ipam = full["ipam_asset_id"].isna()

    # Build final DataFrame
    df = pd.DataFrame({
        "lightspeed_asset_id": range(1, len(full) + 1),
        "obs_asset_id": full["obs_asset_id"],
        "inv_asset_id": full["inv_asset_id"],
        "ipam_asset_id": full["ipam_asset_id"],
        "ip_address": full["obs_ip_address"],
        "hostname": full["obs_hostname"],
        "fqdn": full["obs_fqdn"],
        "status": full["obs_status"],
        "region": full["ipam_region"],
        "vendor": full["inv_vendor"],
        "model": full["inv_model"],
        "missing_in_ipam": missing_in_ipam,
        "missing_in_inventory": missing_in_inventory
    })

    return df

def main():
    if not os.path.exists(DB_FILE):
        raise FileNotFoundError(f"Database not found at {DB_FILE}")

    conn = sqlite3.connect(DB_FILE)

    # Load root tables
    observability = load_table(conn, "observability")
    inventory = load_table(conn, "inventory")
    ipam = load_table(conn, "ipam")

    # Create and save lightspeed_asset
    lightspeed = create_lightspeed_asset(observability, inventory, ipam)
    lightspeed.to_sql("lightspeed_asset", conn, if_exists="replace", index=False)

    conn.commit()
    conn.close()
    print(f"Wrote {len(lightspeed)} records to lightspeed_asset.")

if __name__ == "__main__":
    main()
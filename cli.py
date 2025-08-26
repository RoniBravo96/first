import argparse, os
from career_agent.config import load_config
from career_agent.agent import run_pipeline
from career_agent.database import ensure_db, read_jobs, set_label
from career_agent.feedback import record_feedback_row, train_model_from_feedback

def main():
    ap = argparse.ArgumentParser(description="Career Agent - CLI")
    ap.add_argument("--excel", help="Excel with 'Company Name' & 'Career URL'")
    ap.add_argument("--out", default="out_jobs", help="Output folder")
    ap.add_argument("--config", default="agent_config.json", help="Config JSON path")
    ap.add_argument("--feedback", nargs=4, metavar=("company","title","url","label"), help="Label pos|neg")
    ap.add_argument("--train", action="store_true", help="Train ML model from feedback")
    args = ap.parse_args()

    cfg = load_config(args.config)
    os.makedirs(args.out, exist_ok=True)
    ensure_db(cfg.db_path)

    if args.feedback:
        company, title, url, label = args.feedback
        record_feedback_row(company, title, url, label, os.path.join(args.out, cfg.feedback_csv))
        print("Feedback recorded.")
        return

    if args.train:
        eng = ensure_db(cfg.db_path)
        hist = read_jobs(eng, limit=100000)
        path = train_model_from_feedback(hist, os.path.join(args.out, cfg.feedback_csv), cfg.model_path)
        print("Model trained:", path)
        return

    if not args.excel:
        ap.error("--excel is required unless --train/--feedback used")

    res = run_pipeline(args.excel, args.out, cfg, model_path=(cfg.model_path if os.path.exists(cfg.model_path) else None))
    print("Saved:", os.path.join(args.out, cfg.results_csv))
    if not res.empty:
        print(res.head(20).to_string(index=False))

if __name__ == "__main__":
    main()
    
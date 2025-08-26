import json
from dataclasses import dataclass, field, asdict
from typing import List, Optional

@dataclass
class AgentConfig:
    include_keywords: List[str] = field(default_factory=list)
    exclude_keywords: List[str] = field(default_factory=list)
    locations_whitelist: List[str] = field(default_factory=list)
    locations_blacklist: List[str] = field(default_factory=list)
    remote_ok: bool = True
    junior_signals: List[str] = field(default_factory=list)
    max_companies: int = 200
    request_timeout_sec: int = 20
    user_agent: str = "Mozilla/5.0"
    min_sleep_between_requests: float = 0.8
    max_sleep_between_requests: float = 2.2
    feedback_csv: str = "jobs_feedback.csv"
    history_csv: str = "jobs_history.csv"
    results_csv: str = "jobs_results.csv"
    excel_sheet: Optional[str] = None
    excel_company_col: str = "Company Name"
    excel_url_col: str = "Career URL"
    db_path: str = "out_jobs/jobs.sqlite"
    model_path: str = "out_jobs/model.joblib"

    selenium_enabled: bool = False
    selenium_headless: bool = True

    telegram_bot_token: str = ""
    telegram_chat_id: str = ""

def load_config(path: str) -> AgentConfig:
    with open(path, "r", encoding="utf-8") as f:
        d = json.load(f)
    return AgentConfig(**d)

def save_config(cfg: AgentConfig, path: str):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(asdict(cfg), f, ensure_ascii=False, indent=2)

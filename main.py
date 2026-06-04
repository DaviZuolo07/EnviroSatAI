# main.py

from config.scenarios import SCENARIO_MENU, Scenario
from src.orchestrators.mission_orchestrator import MissionOrchestrator
from src.utils.logger import get_logger

logger = get_logger(__name__)
orchestrator = MissionOrchestrator()

def exibir_menu():
    print("\n" + "="*60)
    print("  ENVIROSAT AI — CENTRO DE CONTROLE AMBIENTAL")
    print("="*60)
    print("\n  Selecione o cenário operacional:\n")
    for key, (_, label) in SCENARIO_MENU.items():
        print(f"  [{key}] {label}")
    print("\n  [0] Sair\n")

def exibir_resultado(result):
    t = result.telemetry
    a = result.assessment

    print(f"\n{'='*60}")
    print(f"  CICLO — {result.scenario.name}")
    print(f"{'='*60}\n")

    print("📡 TELEMETRIA:")
    for campo, valor in t.__dict__.items():
        print(f"   {campo}: {valor}")

    print(f"\n⚠️  RISK SCORE: {a.score}/100 — {a.severity}")
    for alert in a.active_alerts:
        print(f"   → {alert}")
    for action in a.automated_actions:
        print(f"   ✓ {action}")

    print("\n🤖 ARIA:")
    print(result.llm_analysis)

def main():
    while True:
        exibir_menu()
        escolha = input("  Cenário: ").strip()

        if escolha == "0":
            print("\n  Encerrando EnviroSat AI.\n")
            break
        elif escolha in SCENARIO_MENU:
            scenario, _ = SCENARIO_MENU[escolha]
            result = orchestrator.executar_ciclo(scenario)
            exibir_resultado(result)
            input("\n  [ENTER] para voltar ao menu...")
        else:
            print("\n  Opção inválida.")

if __name__ == "__main__":
    main()
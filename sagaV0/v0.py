class SagaStep:
    def __init__(self, name, action, compensation):
        self.name = name
        self.action = action
        self.compensation = compensation

    def execute(self):
        print(f"执行步骤: {self.name}")
        self.action()

    def compensate(self):
        print(f"执行补偿: {self.name}")
        self.compensation()


class Saga:
    def __init__(self, steps):
        self.steps = steps
        self.completed_steps = []

    def execute(self):
        try:
            for step in self.steps:
                step.execute()
                self.completed_steps.append(step)
            print("✅ Saga 执行成功")
        except Exception as e:
            print(f"❌ Saga 执行失败: {e}")
            self.rollback()

    def rollback(self):
        print("开始执行补偿事务...")
        for step in reversed(self.completed_steps):
            try:
                step.compensate()
            except Exception as e:
                print(f"补偿失败: {step.name}, 错误: {e}")
        print("补偿事务完成")


# 以下是业务逻辑的模拟函数
def create_order():
    print("创建订单成功")

def cancel_order():
    print("取消订单成功")

def reserve_inventory():
    print("库存预留成功")
    # 模拟失败，抛异常测试补偿
    # raise Exception("库存不足")

def release_inventory():
    print("库存释放成功")

def process_payment():
    print("支付处理成功")
    # 模拟支付失败，触发补偿
    raise Exception("支付失败")

def refund_payment():
    print("支付退款成功")


if __name__ == "__main__":
    steps = [
        SagaStep("创建订单", create_order, cancel_order),
        SagaStep("预留库存", reserve_inventory, release_inventory),
        SagaStep("处理支付", process_payment, refund_payment),
    ]

    saga = Saga(steps)
    saga.execute()

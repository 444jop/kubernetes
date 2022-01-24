# 쿠버네티스는 동일한 클러스터 내에서 재생성 및 롤링배포만 지원한다.
Istio와 같은 서비스 메시는 트래픽 관리 및 카나리아 배포에 사용할 수 있다.

## 배포전략

* Recreate : 기존버전을 완전히 삭제 후 새로운 버전을 생성하여 배포한다.
  - 해당 방식의 문제는 기존버전이 완전히 삭제되고 새로운 버전이 올라가는 중에는
    사용자들이 액세스 할 수 없어 서비스연속성이 깨지게 된다.

* Rolling Update : 기존 버전을 하나씩 내리고 새로운 버전을 하나씩 올려서
  사용자들이 새로운 업데이트 버전이 생성되는동안 기존 시스템을 사용하면서
  서비스 연속성이 유지된다.
  롤링 업데이트가 default 배포 전략이다.

위 두가지 배포 전략 이외에 다른 배포 방식이 있다.

## 블루그린 배포
  기존 버전을 Blue, 새로운 버전이 Green
  ㅇ

  - kubernetes 에서의 blue / green 배포
    - blue-deployment(lables -> version:v1) 생성 및 서비스 생성 , 레이블 연동
    - green-deployment(labels -> version:v2) 생성
    - 서비스의 레이블을 기존 version:v1 에서 version:v2로 변경
    - 블루그린 배포의 단점으로 생각되는 것 : 리소스가 2배로 든다
      구버전과 신버전을 동시에 유지하여야 하므로 배수가 됨

## 카나리 업데이트
  기존 버전을 그대로 서비스 하면서 새로운 버전을 기존버전에 조금씩 밀어넣는다.
  새로운 버전을 테스트 하면서, 테스트 결과가 만족스럽다면 기존버전을 하나씩 제거하면서 새로운 버전으로 롤링업데이트 한다.
  
  - kubernetes 에서의 canary 배포
    - origin-deployment(labels ->version:v1) replicas=5
    - canary-deployment(lables ->version:v2) replicas=5
    - 서비스에서 두군데 모두로 트래픽을 보내기 위해 공통의 레이블을 생성한다.
    - origin-deployment(labels -> version:v1 , app:front-end)
    - canary-deployment(labels -> version:v2, app:front-end)
    - 서비스에서 셀럭트 값을 version:vX가 아닌 app:front-end로 변경
    - 이렇게 설정시에 각 디플로이먼트에 대해 50:50 으로 분산을 시킨다.
    - 처음에 의도한것은 새로운 카나리 디플로이먼트에는 적은 비율로 트래픽을 보내길 원함
    - 그래서 카나리 디플로이먼트의 레플리카 수를 줄여 처리되는 트래픽의 양을 줄인다.
    - origin-deployment : canary-deployment = 5:1
    - 83% : 17% 비율로 트래픽을 처리하게 된다.
    - 예를들어 99퍼센트의 기존 서비스와 새로운서비스를 1퍼센트로 유지하려고 한다면 합계 100개의 POD를 이용하여 배포를 진행해야 하지만 서비스메시의 제어를 통하면 POD의 갯수에 상관없이 원하는 비율로 트래픽 조정이 가능하다.
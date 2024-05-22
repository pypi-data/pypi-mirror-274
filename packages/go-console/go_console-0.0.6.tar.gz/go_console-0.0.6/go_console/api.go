package extract

import (
	"encoding/json"
	"fmt"
	"net/http"
	"reflect"
	"strings"
	"sync"

	"git.code.oa.com/trpc-go/trpc-go"
	"git.code.oa.com/trpc-go/trpc-go/admin"
	"git.code.oa.com/trpc-go/trpc-go/log"
	"github.com/traefik/yaegi/interp"
	"github.com/traefik/yaegi/stdlib"
)

var Symbols = map[string]map[string]reflect.Value{}

type Req struct {
	Command     string   `json:"command"`
	Requirement []string `json:"requirement"`
}
type Rsp struct {
	Result string `json:"result"`
}

type Console struct {
	out         strings.Builder
	interpreter *interp.Interpreter
	once        sync.Once

	localVar map[string]reflect.Value
}

func New() *Console {
	return &Console{
		once: sync.Once{},
	}
}

func (c *Console) initInterpreter() {
	c.once.Do(func() {
		c.interpreter = interp.New(interp.Options{
			Stdout: &c.out,
		})
		_ = c.interpreter.Use(stdlib.Symbols)
		_ = c.interpreter.Use(Symbols)
		_ = c.interpreter.Use(map[string]map[string]reflect.Value{
			"local/local": c.localVar,
		})
	})
}

func (c *Console) runHandle(w http.ResponseWriter, r *http.Request) {
	decoder := json.NewDecoder(r.Body)
	req := Req{}
	err := decoder.Decode(&req)
	if err != nil {
		log.Errorf("err req body:%v", r.Body)
		return
	}
	ctx := trpc.BackgroundContext()
	c.initInterpreter()
	log.Info(req.Requirement)
	for _, name := range req.Requirement {
		_, err := c.interpreter.Eval(fmt.Sprintf("import \"%s\"", name))
		if err != nil {
			log.ErrorContext(ctx, err)
			c.out.WriteString(fmt.Sprintf("[Import Error] %v\n", err))
			return
		}
	}
	res, err := c.interpreter.Eval(req.Command)
	if err != nil {
		log.ErrorContext(ctx, err)
		c.out.WriteString(fmt.Sprintf("[Error] %v\n", err))
		return
	}
	rsp, err := json.Marshal(Rsp{
		Result: res.String(),
	})
	if err != nil {
		log.Errorf("err marshal:%v", err)
	}
	_, _ = w.Write(rsp)
}

func (c *Console) consoleHandle(w http.ResponseWriter, r *http.Request) {
	rsp := Rsp{
		Result: c.out.String(),
	}
	rspData, err := json.Marshal(rsp)
	if err != nil {
		log.Errorf("err marshal:%v", err)
	}
	_, _ = w.Write(rspData)
}

func (c *Console) cleanHandle(w http.ResponseWriter, r *http.Request) {
	c.once = sync.Once{}
	c.out.Reset()
}

func (c *Console) packagesHandle(w http.ResponseWriter, r *http.Request) {
	sym := Symbols
	res := make(map[string][]string, len(sym))
	for packageName, packageContent := range sym {
		for symbol, _ := range packageContent {
			res[packageName] = append(res[packageName], symbol)
		}
	}
	rspData, err := json.Marshal(res)
	if err != nil {
		log.Errorf("err marshal:%v", err)
	}
	_, _ = w.Write(rspData)
}

func (c *Console) Init(v map[string]any) {
	admin.HandleFunc("/cmds/run", c.runHandle)
	admin.HandleFunc("/cmds/packages", c.packagesHandle)
	admin.HandleFunc("/cmds/console", c.consoleHandle)
	admin.HandleFunc("/cmds/clean", c.cleanHandle)
	c.localVar = make(map[string]reflect.Value)
	for n, v := range v {
		c.localVar[n] = reflect.ValueOf(v)
	}
}
